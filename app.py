import streamlit as st
import requests
from datetime import datetime

# ==========================================
# Configuração Geral da Aplicação
# ==========================================
st.set_page_config(
    page_title="EduTrack AI - Gestão Acadêmica",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Inicialização do Estado (Session State)
# ==========================================
# Garante persistência em memória caso o backend Xano ainda não tenha
# os endpoints publicados ou esteja em modo de prototipação offline.
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {
            "id": 1,
            "code": "INNOV-101",
            "name": "Innovation Lab - Projeto Aplicado",
            "description": "Desenvolvimento prático de soluções tecnológicas de alto impacto com IA na Faculdade Impacta.",
            "workload_hours": 80,
            "teacher_name": "Prof. Coordenador de Inovação",
            "created_at": "2026-09-01T10:00:00Z"
        },
        {
            "id": 2,
            "code": "IA-201",
            "name": "Inteligência Artificial e Machine Learning",
            "description": "Estudo de modelos preditivos, agentes autônomos, LLMs e orquestração de microsserviços.",
            "workload_hours": 60,
            "teacher_name": "Dra. Juliana Costa",
            "created_at": "2026-09-05T14:30:00Z"
        },
        {
            "id": 3,
            "code": "ENG-301",
            "name": "Engenharia de Software e Arquitetura",
            "description": "Padrões de projeto, arquitetura REST, boas práticas de versionamento e OpenSpec.",
            "workload_hours": 80,
            "teacher_name": "Prof. Roberto Mendes",
            "created_at": "2026-09-10T09:15:00Z"
        }
    ]

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "Modelar tabela subject no Xano",
            "subject_code": "INNOV-101",
            "priority": "Alta",
            "completed": True,
            "due_date": "2026-09-25"
        },
        {
            "id": 2,
            "title": "Implementar endpoints CRUD de disciplinas",
            "subject_code": "ENG-301",
            "priority": "Alta",
            "completed": False,
            "due_date": "2026-09-28"
        },
        {
            "id": 3,
            "title": "Estudar fluxo de orquestração de agentes e OpenSpec",
            "subject_code": "IA-201",
            "priority": "Média",
            "completed": False,
            "due_date": "2026-10-02"
        }
    ]

if "editing_subject_id" not in st.session_state:
    st.session_state.editing_subject_id = None

# ==========================================
# Funções de Integração (Xano API & Fallback)
# ==========================================
def test_xano_connection(api_url):
    """Testa se o endpoint base do Xano está respondendo."""
    if not api_url:
        return False, "Nenhuma URL informada."
    try:
        response = requests.get(api_url, timeout=3)
        if response.status_code in [200, 401, 404]:
            return True, f"Conexão bem sucedida (HTTP {response.status_code})."
        return False, f"Resposta inesperada do servidor: HTTP {response.status_code}"
    except Exception as e:
        return False, f"Falha ao conectar: {str(e)}"

def get_all_subjects(api_url, use_xano=False):
    """Obtém a lista de disciplinas (GET /subjects)."""
    if use_xano and api_url:
        try:
            url = f"{api_url.rstrip('/')}/subjects"
            res = requests.get(url, timeout=4)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return st.session_state.subjects

def add_subject(api_url, subject_data, use_xano=False):
    """Cria uma nova disciplina (POST /subjects)."""
    # Validações obrigatórias conforme proposal.md e spec.md
    name = subject_data.get("name", "").strip()
    code = subject_data.get("code", "").strip().upper()
    
    if not name:
        return False, "O nome da disciplina é obrigatório."
    if not code:
        return False, "O código da disciplina é obrigatório."
    
    # Verifica unicidade do código (Scenario: Duplicate subject code)
    existing_codes = [s["code"].upper() for s in st.session_state.subjects]
    if code in existing_codes:
        return False, f"Já existe uma disciplina com o código '{code}'. O código deve ser único."

    if use_xano and api_url:
        try:
            url = f"{api_url.rstrip('/')}/subjects"
            payload = {
                "name": name,
                "code": code,
                "description": subject_data.get("description", "").strip(),
                "workload_hours": subject_data.get("workload_hours"),
                "teacher_id": subject_data.get("teacher_id")
            }
            res = requests.post(url, json=payload, timeout=5)
            if res.status_code in [200, 201]:
                return True, "Disciplina cadastrada com sucesso no Xano!"
            else:
                return False, f"Erro Xano ({res.status_code}): {res.text}"
        except Exception as e:
            return False, f"Erro ao comunicar com Xano: {str(e)}"
    
    # Armazena no session_state
    new_id = max([s["id"] for s in st.session_state.subjects], default=0) + 1
    new_record = {
        "id": new_id,
        "name": name,
        "code": code,
        "description": subject_data.get("description", "").strip(),
        "workload_hours": subject_data.get("workload_hours"),
        "teacher_name": subject_data.get("teacher_name", "").strip() or "Não atribuído",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    st.session_state.subjects.append(new_record)
    return True, "Disciplina cadastrada com sucesso!"

def update_subject(api_url, subject_id, updated_data, use_xano=False):
    """Atualiza uma disciplina existente (PATCH /subjects/{id})."""
    name = updated_data.get("name", "").strip()
    code = updated_data.get("code", "").strip().upper()
    
    if not name:
        return False, "O nome não pode ficar vazio."
    if not code:
        return False, "O código não pode ficar vazio."
    
    # Verifica unicidade com outros registros
    for s in st.session_state.subjects:
        if s["id"] != subject_id and s["code"].upper() == code:
            return False, f"O código '{code}' já está sendo usado por outra disciplina."
            
    if use_xano and api_url:
        try:
            url = f"{api_url.rstrip('/')}/subjects/{subject_id}"
            res = requests.patch(url, json=updated_data, timeout=5)
            if res.status_code == 200:
                return True, "Disciplina atualizada no Xano com sucesso!"
            return False, f"Erro Xano ({res.status_code}): {res.text}"
        except Exception as e:
            return False, f"Erro ao atualizar no Xano: {str(e)}"
            
    for s in st.session_state.subjects:
        if s["id"] == subject_id:
            s["name"] = name
            s["code"] = code
            s["description"] = updated_data.get("description", "").strip()
            s["workload_hours"] = updated_data.get("workload_hours")
            s["teacher_name"] = updated_data.get("teacher_name", "").strip() or "Não atribuído"
            return True, "Disciplina atualizada com sucesso!"
    return False, "Disciplina não encontrada."

def delete_subject(api_url, subject_id, use_xano=False):
    """Remove uma disciplina cadastrada (DELETE /subjects/{id})."""
    if use_xano and api_url:
        try:
            url = f"{api_url.rstrip('/')}/subjects/{subject_id}"
            res = requests.delete(url, timeout=5)
            if res.status_code == 200:
                return True, "Disciplina removida no Xano com sucesso!"
            return False, f"Erro Xano ({res.status_code}): {res.text}"
        except Exception as e:
            return False, f"Erro ao deletar no Xano: {str(e)}"

    st.session_state.subjects = [s for s in st.session_state.subjects if s["id"] != subject_id]
    return True, "Disciplina excluída com sucesso!"

# ==========================================
# Sidebar (Navegação e Conexão)
# ==========================================
with st.sidebar:
    st.title("🎓 EduTrack AI")
    st.caption("Innovation Lab – Faculdade Impacta")
    st.divider()

    menu_option = st.radio(
        "Navegação",
        ["📊 Dashboard", "📚 Disciplinas", "✅ Tarefas"],
        index=0
    )

    st.divider()
    with st.expander("⚙️ Conexão com Backend (Xano)"):
        api_base_url = st.text_input(
            "URL Base da API Xano",
            value="https://x8ki-letl-twmt.n7.xano.io/api:subjects",
            help="URL dos endpoints do Xano criados conforme proposal.md e tasks.md"
        )
        use_xano = st.toggle("Sincronizar com Xano", value=False)
        if st.button("Testar Conexão"):
            ok, msg = test_xano_connection(api_base_url)
            if ok:
                st.success(msg)
            else:
                st.warning(msg)
        
        if use_xano:
            st.info("🌐 Modo Online (Xano API Ativa)")
        else:
            st.success("🟢 Modo Local Ativo (Memória Dinâmica)")

# ==========================================
# Página 1: Dashboard
# ==========================================
if menu_option == "📊 Dashboard":
    st.title("📊 Painel de Controle Acadêmico")
    st.write("Acompanhe o desempenho de disciplinas, carga horária e entregas de atividades.")

    subjects_list = get_all_subjects(api_base_url, use_xano)
    total_subjects = len(subjects_list)
    total_hours = sum([int(s.get("workload_hours") or 0) for s in subjects_list])
    
    pending_tasks = len([t for t in st.session_state.tasks if not t.get("completed")])
    completed_tasks = len([t for t in st.session_state.tasks if t.get("completed")])

    # Métricas principais em destaque
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Disciplinas Ativas", str(total_subjects), help="Total de componentes curriculares cadastrados")
    col2.metric("Carga Horária Total", f"{total_hours}h", help="Soma das horas de aula do semestre")
    col3.metric("Tarefas Pendentes", str(pending_tasks), delta=f"-{pending_tasks}" if pending_tasks > 0 else "0", delta_color="inverse")
    col4.metric("Tarefas Concluídas", str(completed_tasks), delta=f"+{completed_tasks}")

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📚 Disciplinas em Andamento")
        if subjects_list:
            for s in subjects_list:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"**{s.get('name')}** (`{s.get('code')}`)")
                    c1.caption(f"Docente: {s.get('teacher_name', 'N/A')} • {s.get('description', '')}")
                    c2.markdown(f"**{s.get('workload_hours', 0)}h**")
        else:
            st.info("Nenhuma disciplina cadastrada ainda. Vá para a aba 'Disciplinas' para cadastrar!")

    with col_right:
        st.subheader("📌 Próximas Entregas")
        upcoming = [t for t in st.session_state.tasks if not t.get("completed")]
        if upcoming:
            for t in upcoming:
                with st.container(border=True):
                    st.markdown(f"**{t['title']}**")
                    st.caption(f"Disciplina: `{t['subject_code']}` | Prazo: {t['due_date']} | Prioridade: {t['priority']}")
        else:
            st.success("🎉 Todas as tarefas estão em dia!")

# ==========================================
# Página 2: Disciplinas (Subjects - proposal.md & tasks.md)
# ==========================================
elif menu_option == "📚 Disciplinas":
    st.title("📚 Gerenciamento de Disciplinas")
    st.markdown(
        "Módulo de gestão curricular para catálogo e manutenção de disciplinas acadêmicas "
        "(conforme especificado em `proposal.md` e `tasks.md`)."
    )

    tab_list, tab_create = st.tabs(["📋 Catálogo de Disciplinas", "➕ Cadastrar Nova Disciplina"])

    # ------------------------------------------
    # Aba 1: Listagem, Busca, Edição e Exclusão
    # ------------------------------------------
    with tab_list:
        subjects_list = get_all_subjects(api_base_url, use_xano)

        # Barra de Pesquisa e Filtros (GET /subjects com busca)
        search_query = st.text_input("🔍 Buscar por nome ou código da disciplina:", placeholder="Ex: IA, INNOV, Engenharia...")
        
        filtered_subjects = subjects_list
        if search_query:
            filtered_subjects = [
                s for s in subjects_list
                if search_query.lower() in s.get("name", "").lower() or search_query.lower() in s.get("code", "").lower()
            ]

        st.caption(f"Exibindo {len(filtered_subjects)} de {len(subjects_list)} disciplina(s) cadastrada(s).")

        # Formulário de edição rápida caso uma disciplina esteja selecionada
        if st.session_state.editing_subject_id is not None:
            sub_to_edit = next((s for s in st.session_state.subjects if s["id"] == st.session_state.editing_subject_id), None)
            if sub_to_edit:
                with st.form("form_edit_subject"):
                    st.subheader(f"✏️ Editando: {sub_to_edit['name']} ({sub_to_edit['code']})")
                    e_col1, e_col2 = st.columns([3, 1])
                    edit_name = e_col1.text_input("Nome da Disciplina*", value=sub_to_edit["name"])
                    edit_code = e_col2.text_input("Código*", value=sub_to_edit["code"])
                    
                    e_col3, e_col4 = st.columns([2, 1])
                    edit_teacher = e_col3.text_input("Professor Responsável", value=sub_to_edit.get("teacher_name", ""))
                    edit_workload = e_col4.number_input("Carga Horária (horas)", value=int(sub_to_edit.get("workload_hours") or 60), min_value=1, step=10)
                    
                    edit_desc = st.text_area("Descrição da Ementa", value=sub_to_edit.get("description", ""))
                    
                    btn_save, btn_cancel = st.columns([1, 1])
                    with btn_save:
                        submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
                    with btn_cancel:
                        cancel = st.form_submit_button("Cancelar", use_container_width=True)

                    if submitted:
                        ok, msg = update_subject(
                            api_base_url,
                            sub_to_edit["id"],
                            {
                                "name": edit_name,
                                "code": edit_code,
                                "teacher_name": edit_teacher,
                                "workload_hours": edit_workload,
                                "description": edit_desc
                            },
                            use_xano
                        )
                        if ok:
                            st.session_state.editing_subject_id = None
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    if cancel:
                        st.session_state.editing_subject_id = None
                        st.rerun()

        # Renderização dos Cards de Disciplinas
        if not filtered_subjects:
            st.info("Nenhuma disciplina encontrada com os critérios pesquisados.")
        else:
            for subject in filtered_subjects:
                with st.container(border=True):
                    header_col, action_col = st.columns([4, 1.2])
                    
                    with header_col:
                        st.markdown(f"### `{subject.get('code')}` - {subject.get('name')}")
                        st.caption(f"👨‍🏫 **Professor Responsável:** {subject.get('teacher_name', 'Não atribuído')} | ⏱️ **Carga Horária:** {subject.get('workload_hours', 0)} horas")
                        if subject.get("description"):
                            st.write(subject.get("description"))
                        if subject.get("created_at"):
                            st.caption(f"🗓️ Cadastrada em: {subject.get('created_at')[:10]}")

                    with action_col:
                        st.write("")
                        c_edit, c_del = st.columns(2)
                        with c_edit:
                            if st.button("✏️ Editar", key=f"edit_{subject['id']}", use_container_width=True):
                                st.session_state.editing_subject_id = subject["id"]
                                st.rerun()
                        with c_del:
                            if st.button("🗑️ Excluir", key=f"del_{subject['id']}", use_container_width=True, type="secondary"):
                                ok, msg = delete_subject(api_base_url, subject["id"], use_xano)
                                if ok:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)

    # ------------------------------------------
    # Aba 2: Cadastro de Nova Disciplina (POST /subjects)
    # ------------------------------------------
    with tab_create:
        st.subheader("➕ Formulário de Cadastro de Disciplina")
        st.caption("Preencha as informações para registrar um novo componente curricular no sistema.")

        with st.form("create_subject_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns([3, 1])
            new_name = f_col1.text_input("Nome da Disciplina*", placeholder="Ex: Algoritmos e Estrutura de Dados")
            new_code = f_col2.text_input("Código da Disciplina*", placeholder="Ex: ED-102")

            f_col3, f_col4 = st.columns([2, 1])
            new_teacher = f_col3.text_input("Professor Responsável (teacher_id / nome)", placeholder="Ex: Prof. Dr. Alan Turing")
            new_workload = f_col4.number_input("Carga Horária (horas)", min_value=0, max_value=400, value=80, step=10)

            new_desc = st.text_area("Descrição / Ementa Curricular", placeholder="Breve resumo dos tópicos abordados na disciplina...")

            submit_btn = st.form_submit_button("Cadastrar Disciplina", type="primary", use_container_width=True)

            if submit_btn:
                data = {
                    "name": new_name,
                    "code": new_code,
                    "teacher_name": new_teacher,
                    "workload_hours": new_workload,
                    "description": new_desc
                }
                success, message = add_subject(api_base_url, data, use_xano)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# ==========================================
# Página 3: Tarefas (Tasks)
# ==========================================
elif menu_option == "✅ Tarefas":
    st.title("✅ Gerenciamento de Tarefas Acadêmicas")
    st.write("Organize entregas, projetos e estudos vinculados às disciplinas curriculares.")

    tab_tasks_list, tab_tasks_new = st.tabs(["📋 Lista de Tarefas", "➕ Criar Nova Tarefa"])

    subjects_list = get_all_subjects(api_base_url, use_xano)
    subject_codes = [s["code"] for s in subjects_list] or ["GERAL"]

    # ------------------------------------------
    # Aba 1: Lista e Interação de Tarefas
    # ------------------------------------------
    with tab_tasks_list:
        filter_col1, filter_col2 = st.columns([2, 2])
        status_filter = filter_col1.selectbox("Filtrar por Status:", ["Todas", "Pendentes", "Concluídas"])
        subject_filter = filter_col2.selectbox("Filtrar por Disciplina:", ["Todas"] + subject_codes)

        tasks_to_show = st.session_state.tasks
        if status_filter == "Pendentes":
            tasks_to_show = [t for t in tasks_to_show if not t["completed"]]
        elif status_filter == "Concluídas":
            tasks_to_show = [t for t in tasks_to_show if t["completed"]]

        if subject_filter != "Todas":
            tasks_to_show = [t for t in tasks_to_show if t["subject_code"] == subject_filter]

        st.caption(f"Mostrando {len(tasks_to_show)} tarefa(s).")

        if not tasks_to_show:
            st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
        else:
            for task in tasks_to_show:
                with st.container(border=True):
                    check_col, info_col, del_col = st.columns([0.5, 4, 0.8])
                    
                    with check_col:
                        done = st.checkbox(
                            "",
                            value=task["completed"],
                            key=f"task_check_{task['id']}",
                            label_visibility="collapsed"
                        )
                        if done != task["completed"]:
                            task["completed"] = done
                            st.rerun()

                    with info_col:
                        if task["completed"]:
                            st.markdown(f"~~**{task['title']}**~~")
                        else:
                            st.markdown(f"**{task['title']}**")
                        st.caption(
                            f"Disciplina: `{task['subject_code']}` | "
                            f"Prazo: {task['due_date']} | "
                            f"Prioridade: **{task['priority']}**"
                        )

                    with del_col:
                        if st.button("🗑️", key=f"del_task_{task['id']}", help="Excluir tarefa"):
                            st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                            st.rerun()

    # ------------------------------------------
    # Aba 2: Criação de Nova Tarefa
    # ------------------------------------------
    with tab_tasks_new:
        st.subheader("➕ Adicionar Nova Tarefa")
        with st.form("form_new_task", clear_on_submit=True):
            task_title = st.text_input("Título da Tarefa*", placeholder="Ex: Entrega do Modelo de Dados Xano")
            t_col1, t_col2, t_col3 = st.columns(3)
            
            task_subject = t_col1.selectbox("Disciplina Associada*", subject_codes)
            task_priority = t_col2.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            task_due = t_col3.date_input("Data de Entrega", datetime.today())

            submit_task = st.form_submit_button("Salvar Tarefa", type="primary", use_container_width=True)

            if submit_task:
                if not task_title.strip():
                    st.error("O título da tarefa é obrigatório.")
                else:
                    new_task_id = max([t["id"] for t in st.session_state.tasks], default=0) + 1
                    st.session_state.tasks.append({
                        "id": new_task_id,
                        "title": task_title.strip(),
                        "subject_code": task_subject,
                        "priority": task_priority,
                        "completed": False,
                        "due_date": task_due.strftime("%Y-%m-%d")
                    })
                    st.success("Tarefa adicionada com sucesso!")
                    st.rerun()
