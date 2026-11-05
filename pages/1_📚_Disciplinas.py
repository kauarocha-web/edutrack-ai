import streamlit as st
from datetime import datetime
from services.api_service import get_subjects, create_subject

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="Disciplinas - EduTrack AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Gestão de Disciplinas")
st.caption("Consulte e cadastre disciplinas acadêmicas integradas à API do Xano.")

# ==============================================================================
# Verificação de Autenticação
# ==============================================================================
token = st.session_state.get("auth_token")

if not token:
    st.warning("🔒 Você precisa estar logado para gerenciar suas disciplinas.")
    st.info("Por favor, acesse a página **👤 Perfil** no menu lateral para fazer login ou criar sua conta.")
    st.stop()

# ==============================================================================
# Interface em Abas: Listagem e Cadastro
# ==============================================================================
tab_lista, tab_novo = st.tabs(["📋 Catálogo de Disciplinas", "➕ Nova Disciplina"])

# ------------------------------------------------------------------------------
# Aba 1: Listagem das Disciplinas (GET /subjects)
# ------------------------------------------------------------------------------
with tab_lista:
    st.subheader("Disciplinas Cadastradas")
    
    # Feedback visual de loading durante a chamada à API
    with st.spinner("Carregando disciplinas do Xano..."):
        success, subjects_data, status_code = get_subjects(token)

    if not success:
        if status_code == 401:
            st.error("⚠️ Sua sessão expirou. Por favor, acesse a página **👤 Perfil** para realizar login novamente.")
        else:
            st.error(f"Erro ao carregar disciplinas: {subjects_data}")
    else:
        if not subjects_data or len(subjects_data) == 0:
            st.info("Nenhuma disciplina cadastrada ainda. Acesse a aba **➕ Nova Disciplina** para adicionar seu primeiro componente curricular!")
        else:
            st.caption(f"Total de {len(subjects_data)} disciplina(s) encontrada(s).")
            
            # Barra de busca rápida
            search_query = st.text_input("🔍 Buscar disciplina por nome ou professor:", placeholder="Digite para filtrar...")
            
            filtered_subjects = subjects_data
            if search_query:
                filtered_subjects = [
                    s for s in subjects_data
                    if search_query.lower() in str(s.get("name", "")).lower() or
                       search_query.lower() in str(s.get("teacher", "")).lower()
                ]

            for s in filtered_subjects:
                with st.container(border=True):
                    col_info, col_hours = st.columns([4, 1])
                    with col_info:
                        st.markdown(f"### {s.get('name', 'Sem Nome')}")
                        st.caption(f"👨‍🏫 **Professor(a):** {s.get('teacher') or 'Não informado'}")
                        
                        created_at = s.get("created_at")
                        if created_at:
                            try:
                                if isinstance(created_at, (int, float)):
                                    dt_str = datetime.fromtimestamp(created_at / 1000).strftime("%d/%m/%Y")
                                else:
                                    dt_str = str(created_at)[:10]
                                st.caption(f"🗓️ Cadastrada em: {dt_str}")
                            except Exception:
                                pass
                    with col_hours:
                        st.metric(label="Carga Horária", value=f"{s.get('hours', 0)}h")

# ------------------------------------------------------------------------------
# Aba 2: Cadastro de Nova Disciplina (POST /subjects)
# ------------------------------------------------------------------------------
with tab_novo:
    st.subheader("Cadastrar Nova Disciplina no Xano")
    st.caption("Preencha as informações abaixo para persistir o novo registro diretamente no backend.")

    with st.form("form_create_subject", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            name = st.text_input("Nome da Disciplina*", placeholder="Ex: Engenharia de Software e Arquitetura")
            teacher = st.text_input("Professor(a) Responsável", placeholder="Ex: Prof. Roberto Mendes")
        with col2:
            hours = st.number_input("Carga Horária (horas)*", min_value=1, max_value=500, value=60, step=10)

        submitted = st.form_submit_button("Salvar no Xano", type="primary", use_container_width=True)

        if submitted:
            if not name.strip():
                st.warning("O nome da disciplina é obrigatório.")
            else:
                with st.spinner("Salvando disciplina no Xano..."):
                    ok, result, status = create_subject(
                        token=token,
                        name=name,
                        teacher=teacher,
                        hours=hours
                    )
                if ok:
                    st.success(f"✅ Disciplina '{name}' cadastrada com sucesso no Xano!")
                    st.rerun()
                else:
                    if status == 401:
                        st.error("⚠️ Sessão expirada! Por favor, acesse a página **👤 Perfil** para reconectar.")
                    else:
                        st.error(f"❌ {result}")