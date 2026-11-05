import streamlit as st
from datetime import datetime
from services.api_service import (
    get_academic_tasks,
    create_academic_task,
    update_academic_task_status,
    get_subjects
)
from scripts.calculate_progress import calculate_subject_progress

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="Tarefas Acadêmicas - EduTrack AI",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Gestão de Tarefas Acadêmicas")
st.caption("Acompanhe entregas, monitore o progresso das disciplinas e registre atividades.")

# ==============================================================================
# Verificação de Autenticação
# ==============================================================================
token = st.session_state.get("auth_token")

if not token:
    st.warning("🔒 Você precisa estar logado para gerenciar suas tarefas acadêmicas.")
    st.info("Por favor, acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    st.stop()

# ==============================================================================
# Carregamento de Dados da API do Xano com Indicador de Loading
# ==============================================================================
with st.spinner("Carregando tarefas e disciplinas do Xano..."):
    tasks_ok, tasks_data, tasks_status = get_academic_tasks(token)
    subjects_ok, subjects_data, subjects_status = get_subjects(token)

# Tratamento de token expirado (HTTP 401)
if tasks_status == 401 or subjects_status == 401:
    st.error("⚠️ Sua sessão expirou. Por favor, acesse a página **👤 Perfil** para realizar login novamente.")
    st.stop()

if not tasks_ok:
    st.error(f"Erro ao carregar tarefas: {tasks_data}")
    tasks_list = []
else:
    tasks_list = tasks_data if isinstance(tasks_data, list) else []

if not subjects_ok:
    st.warning(f"Aviso: Não foi possível obter as disciplinas vinculadas ({subjects_data}).")
    subjects_list = []
else:
    subjects_list = subjects_data if isinstance(subjects_data, list) else []

# Mapeamento de id para nome da disciplina
subject_map = {s["id"]: s.get("name", f"Disciplina #{s['id']}") for s in subjects_list if "id" in s}

# ==============================================================================
# Interface em Abas: Lista de Tarefas e Criação
# ==============================================================================
tab_lista, tab_novo = st.tabs(["📋 Lista de Tarefas", "➕ Criar Nova Tarefa"])

# ------------------------------------------------------------------------------
# Aba 1: Listagem das Tarefas Acadêmicas e Cálculo de Progresso
# ------------------------------------------------------------------------------
with tab_lista:
    st.subheader("Tarefas Registradas")

    if not tasks_list:
        st.info("Nenhuma tarefa acadêmica cadastrada ainda. Use a aba **➕ Criar Nova Tarefa** para adicionar sua primeira atividade!")
    else:
        # Filtros por status e disciplina
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            status_filter = st.selectbox(
                "Filtrar por Status:",
                ["Todos", "Pendente", "Em Andamento", "Concluída"]
            )
        with f_col2:
            subject_options_filter = ["Todas"] + [s.get("name") for s in subjects_list if s.get("name")]
            subject_filter = st.selectbox("Filtrar por Disciplina:", subject_options_filter)

        # Mapeamento do filtro de status para o valor no banco
        status_code_map = {
            "Pendente": "pending",
            "Em Andamento": "in_progress",
            "Concluída": "completed"
        }

        # ----------------------------------------------------------------------
        # Incorporação da Lógica de Cálculo de Progresso (scripts/calculate_progress.py)
        # ----------------------------------------------------------------------
        if subject_filter != "Todas":
            # Progresso da disciplina selecionada
            selected_sub_id = next((s["id"] for s in subjects_list if s.get("name") == subject_filter), None)
            if selected_sub_id is not None:
                prog = calculate_subject_progress(subject_id=selected_sub_id, tasks_list=tasks_list)
                with st.container(border=True):
                    st.markdown(f"#### 📊 Progresso da Disciplina: **{subject_filter}**")
                    p_c1, p_c2, p_c3, p_c4 = st.columns(4)
                    p_c1.metric("Índice de Progresso", f"{prog['progress_percentage']}%")
                    p_c2.metric("Tarefas Concluídas", str(prog["completed_tasks"]))
                    p_c3.metric("Tarefas Pendentes", str(prog["pending_tasks"]))
                    p_c4.metric("Total de Tarefas", str(prog["total_tasks"]))
                    st.progress(prog["progress_percentage"] / 100.0)
        else:
            # Progresso geral somando todas as disciplinas
            total_all = len(tasks_list)
            completed_statuses = {"completed", "concluída", "concluida", "done"}
            completed_all = len([
                t for t in tasks_list
                if str(t.get("status", "")).strip().lower() in completed_statuses
            ])
            pct_all = round((completed_all / total_all) * 100.0, 2) if total_all > 0 else 0.0

            with st.container(border=True):
                st.markdown("#### 📊 Progresso Geral de Todas as Tarefas")
                p_c1, p_c2, p_c3, p_c4 = st.columns(4)
                p_c1.metric("Progresso Geral", f"{pct_all}%")
                p_c2.metric("Total Concluídas", str(completed_all))
                p_c3.metric("Total Pendentes", str(total_all - completed_all))
                p_c4.metric("Total de Tarefas", str(total_all))
                st.progress(pct_all / 100.0)

            # Detalhamento de progresso por disciplina usando calculate_subject_progress
            if subjects_list:
                with st.expander("📈 Ver Progresso Individual por Disciplina"):
                    for s in subjects_list:
                        s_id = s.get("id")
                        s_prog = calculate_subject_progress(subject_id=s_id, tasks_list=tasks_list)
                        sc1, sc2 = st.columns([3, 1])
                        sc1.write(f"**{s.get('name')}** ({s_prog['completed_tasks']}/{s_prog['total_tasks']} concluídas)")
                        sc2.write(f"**{s_prog['progress_percentage']}%**")
                        st.progress(s_prog["progress_percentage"] / 100.0)

        # ----------------------------------------------------------------------
        # Filtragem e Renderização dos Cards de Tarefas
        # ----------------------------------------------------------------------
        filtered_tasks = tasks_list
        if status_filter != "Todos":
            target_status = status_code_map.get(status_filter, status_filter.lower())
            filtered_tasks = [t for t in filtered_tasks if str(t.get("status", "")).lower() == target_status]

        if subject_filter != "Todas":
            selected_sub_id = next((s["id"] for s in subjects_list if s.get("name") == subject_filter), None)
            if selected_sub_id is not None:
                filtered_tasks = [t for t in filtered_tasks if t.get("subject_id") == selected_sub_id]

        st.caption(f"Mostrando {len(filtered_tasks)} de {len(tasks_list)} tarefa(s).")

        if not filtered_tasks:
            st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
        else:
            for task in filtered_tasks:
                with st.container(border=True):
                    c_check, c_info, c_badge = st.columns([0.6, 3.4, 1.5])

                    raw_status = str(task.get("status", "pending")).lower()
                    is_completed = raw_status == "completed"

                    # Checkbox para alternância rápida entre concluída e pendente
                    with c_check:
                        toggled = st.checkbox(
                            "Concluída",
                            value=is_completed,
                            key=f"check_task_{task['id']}",
                            help="Marcar como concluída ou pendente"
                        )
                        if toggled != is_completed:
                            new_status = "completed" if toggled else "pending"
                            with st.spinner("Atualizando status no Xano..."):
                                up_ok, up_msg, _ = update_academic_task_status(
                                    token=token,
                                    task_id=task["id"],
                                    status=new_status,
                                    task_data=task
                                )
                            if up_ok:
                                st.rerun()
                            else:
                                st.error(f"Erro ao atualizar status: {up_msg}")

                    with c_info:
                        task_title = task.get("title", "Sem título")
                        if is_completed:
                            st.markdown(f"### ~~{task_title}~~")
                        else:
                            st.markdown(f"### {task_title}")

                        desc = task.get("description")
                        if desc and desc != "Sem descrição":
                            st.write(desc)

                        sub_name = subject_map.get(task.get("subject_id"), "Geral / Sem vínculo")
                        due_date = task.get("due_date") or "Não definido"
                        st.caption(f"📚 **Disciplina:** {sub_name} | 🗓️ **Prazo:** {due_date}")

                    # Seletor interativo de status
                    with c_badge:
                        status_options = ["pending", "in_progress", "completed"]
                        current_idx = status_options.index(raw_status) if raw_status in status_options else 0
                        new_status_select = st.selectbox(
                            "Status",
                            status_options,
                            index=current_idx,
                            format_func=lambda s: {"pending": "⏳ Pendente", "in_progress": "🔄 Em Andamento", "completed": "✅ Concluída"}.get(s, s),
                            key=f"select_status_{task['id']}",
                            label_visibility="collapsed"
                        )
                        if new_status_select != raw_status:
                            with st.spinner("Atualizando status no Xano..."):
                                up_ok, up_msg, _ = update_academic_task_status(
                                    token=token,
                                    task_id=task["id"],
                                    status=new_status_select,
                                    task_data=task
                                )
                            if up_ok:
                                st.rerun()
                            else:
                                st.error(f"Erro ao atualizar status: {up_msg}")

# ------------------------------------------------------------------------------
# Aba 2: Cadastro de Nova Tarefa (POST /academic_tasks)
# ------------------------------------------------------------------------------
with tab_novo:
    st.subheader("Cadastrar Nova Tarefa no Xano")
    st.caption("Preencha as informações para registrar a atividade vinculando-a a uma disciplina.")

    if not subjects_list:
        st.info("ℹ️ Nenhuma disciplina cadastrada ainda. Você pode criar tarefas como 'Geral' ou cadastrar matérias primeiro na aba **📚 Disciplinas**.")

    with st.form("form_create_task", clear_on_submit=True):
        title = st.text_input("Título da Tarefa*", placeholder="Ex: Entrega do Projeto Aplicado")
        description = st.text_area("Descrição / Instruções", placeholder="Detalhes, critérios de avaliação ou links da entrega...")

        col1, col2, col3 = st.columns(3)
        with col1:
            if subjects_list:
                sub_choices = {f"{s.get('name', 'Sem Nome')} (ID: {s['id']})": s["id"] for s in subjects_list if "id" in s}
                sub_choices["Nenhuma (Geral)"] = 0
                selected_label = st.selectbox("Disciplina Associada*", list(sub_choices.keys()))
                selected_subject_id = sub_choices[selected_label]
            else:
                st.selectbox("Disciplina Associada*", ["Nenhuma (Geral)"], disabled=True)
                selected_subject_id = 0

        with col2:
            status_choice = st.selectbox(
                "Status Inicial",
                ["pending", "in_progress", "completed"],
                format_func=lambda s: {"pending": "⏳ Pendente", "in_progress": "🔄 Em Andamento", "completed": "✅ Concluída"}.get(s, s)
            )

        with col3:
            due_date_val = st.date_input("Data de Entrega", datetime.today())

        submitted_task = st.form_submit_button("Salvar Tarefa no Xano", type="primary", use_container_width=True)

        if submitted_task:
            if not title.strip():
                st.warning("O título da tarefa é obrigatório.")
            else:
                due_date_str = due_date_val.strftime("%Y-%m-%d") if due_date_val else datetime.now().strftime("%Y-%m-%d")
                clean_description = description.strip() if description and description.strip() else "Sem descrição"

                with st.spinner("Salvando tarefa no Xano..."):
                    ok, result, status = create_academic_task(
                        token=token,
                        title=title.strip(),
                        description=clean_description,
                        due_date=due_date_str,
                        status=status_choice,
                        subject_id=selected_subject_id
                    )

                if ok:
                    st.success(f"✅ Tarefa '{title}' cadastrada com sucesso no Xano!")
                    st.rerun()
                else:
                    if status == 401:
                        st.error("⚠️ Sessão expirada! Por favor, acesse a página **👤 Perfil** para reconectar.")
                    else:
                        st.error(f"❌ {result}")
