import os
import streamlit as st
import requests
from datetime import datetime

# ==============================================================================
# Carregamento de Variáveis de Ambiente (.env)
# ==============================================================================
def load_env_variables():
    """Carrega as variáveis do arquivo .env na raiz do projeto."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_file = os.path.join(root_dir, ".env")
    
    # Tentativa com python-dotenv se disponível
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        return
    except ImportError:
        pass

    # Fallback nativo para leitura de .env caso python-dotenv não esteja instalado
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key not in os.environ:
                        os.environ[key] = val

load_env_variables()

# URL Base padrão definida no .env ou fallback canônico do grupo Authentication
DEFAULT_XANO_AUTH_URL = "https://x8ki-letl-twmt.n7.xano.io/api:72mncMCo"
AUTH_BASE_URL = os.getenv("XANO_AUTH_BASE_URL", DEFAULT_XANO_AUTH_URL).rstrip("/")

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="Perfil e Autenticação - EduTrack AI",
    page_icon="👤",
    layout="wide"
)

# Inicialização das variáveis de sessão
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if "user_info" not in st.session_state:
    st.session_state.user_info = None

# ==============================================================================
# Funções de Integração com a API do Xano
# ==============================================================================
def signup_user(name: str, email: str, password: str):
    """
    Cadastra um novo usuário no backend Xano via POST /auth/signup.
    Persiste os dados na tabela 'user' e retorna o token de autenticação.
    """
    url = f"{AUTH_BASE_URL}/auth/signup"
    payload = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": password
    }
    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code in [200, 201]:
            return True, response.json()
        
        # Tratamento de erro retornado pela API do Xano
        try:
            err_data = response.json()
            message = err_data.get("message") or err_data.get("error") or response.text
        except Exception:
            message = response.text or f"Erro {response.status_code}"
            
        return False, f"Falha no cadastro ({response.status_code}): {message}"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão com o servidor de autenticação: {str(e)}"

def login_user(email: str, password: str):
    """
    Realiza o login do usuário via POST /auth/login.
    Retorna o authToken e o user_id.
    """
    url = f"{AUTH_BASE_URL}/auth/login"
    payload = {
        "email": email.strip().lower(),
        "password": password
    }
    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code == 200:
            return True, response.json()
        
        try:
            err_data = response.json()
            message = err_data.get("message") or err_data.get("error") or response.text
        except Exception:
            message = response.text or f"Erro {response.status_code}"
            
        return False, f"Falha no login ({response.status_code}): {message}"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão com o servidor de autenticação: {str(e)}"

def get_user_profile(token: str):
    """
    Recupera os dados cadastrais do usuário autenticado via GET /auth/me.
    Requer o cabeçalho Authorization: Bearer <token>.
    """
    url = f"{AUTH_BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            return True, response.json()
        return False, f"Erro ao obter dados do usuário ({response.status_code}): {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão ao carregar perfil: {str(e)}"

def logout_user():
    """Limpa os dados de autenticação da sessão do Streamlit."""
    st.session_state.auth_token = None
    st.session_state.user_info = None
    st.rerun()

# ==============================================================================
# Interface do Usuário (Streamlit)
# ==============================================================================
st.title("👤 Perfil do Usuário e Autenticação")
st.caption("Acesso seguro ao EduTrack AI com autenticação integrada ao Xano.")

# Sidebar com informações do endpoint
with st.sidebar:
    st.markdown("### ⚙️ Configurações de Auth")
    st.caption("URL Base definida no arquivo `.env`:")
    st.code(AUTH_BASE_URL, language="text")

# ------------------------------------------------------------------------------
# Caso 1: Usuário Autenticado (Exibição do Perfil e Opção de Logout)
# ------------------------------------------------------------------------------
if st.session_state.auth_token:
    # Se os dados do perfil ainda não foram carregados na sessão, busca no Xano
    if not st.session_state.user_info:
        with st.spinner("Carregando informações do perfil..."):
            success, result = get_user_profile(st.session_state.auth_token)
            if success:
                st.session_state.user_info = result
            else:
                st.error(f"Não foi possível sincronizar o perfil: {result}")

    user = st.session_state.user_info or {}

    st.success("✅ Você está autenticado na plataforma EduTrack AI!")
    st.divider()

    col_info, col_actions = st.columns([3, 1])

    with col_info:
        st.subheader("📋 Informações da Conta")
        
        info_c1, info_c2 = st.columns(2)
        with info_c1:
            st.markdown(f"**Nome:** {user.get('name', 'N/A')}")
            st.markdown(f"**E-mail:** `{user.get('email', 'N/A')}`")
            st.markdown(f"**Identificador (ID):** `{user.get('id', 'N/A')}`")

        with info_c2:
            st.markdown(f"**Papel / Função:** `{user.get('role', 'member')}`")
            
            created_at = user.get("created_at")
            if created_at:
                try:
                    # Converte timestamp caso seja numérico ou data ISO
                    if isinstance(created_at, (int, float)):
                        formatted_date = datetime.fromtimestamp(created_at / 1000).strftime("%d/%m/%Y às %H:%M")
                    else:
                        formatted_date = str(created_at)[:10]
                except Exception:
                    formatted_date = str(created_at)
            else:
                formatted_date = "N/A"
            st.markdown(f"**Membro desde:** {formatted_date}")

    with col_actions:
        st.subheader("🚪 Sessão")
        st.write("Deseja encerrar sua sessão atual?")
        if st.button("Sair da Conta (Logout)", type="secondary", use_container_width=True):
            logout_user()

    st.divider()
    with st.expander("🔍 Detalhes Técnicos da Sessão"):
        st.markdown(f"**Endpoint Conectado:** `{AUTH_BASE_URL}/auth/me`")
        st.markdown(f"**Token JWT (Bearer):** `{st.session_state.auth_token[:25]}...`")

# ------------------------------------------------------------------------------
# Caso 2: Usuário Não Autenticado (Formulários de Login e Cadastro)
# ------------------------------------------------------------------------------
else:
    st.info("Entre com suas credenciais ou crie uma nova conta para acessar os recursos personalizados.")

    tab_login, tab_signup = st.tabs(["🔑 Entrar na Conta (Login)", "📝 Criar Nova Conta (Cadastro)"])

    # --------------------------------------------------------------------------
    # Aba 1: Formulário de Login (POST /auth/login)
    # --------------------------------------------------------------------------
    with tab_login:
        st.subheader("Acesse sua Conta")
        with st.form("form_login"):
            login_email = st.text_input("E-mail Cadastrado", placeholder="exemplo@faculdadeimpacta.com.br")
            login_password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            btn_login = st.form_submit_button("Entrar", type="primary", use_container_width=True)

            if btn_login:
                if not login_email.strip() or not login_password:
                    st.warning("Por favor, preencha o e-mail e a senha.")
                else:
                    with st.spinner("Autenticando..."):
                        success, result = login_user(login_email, login_password)
                        if success:
                            token = result.get("authToken")
                            st.session_state.auth_token = token
                            
                            # Carrega os dados do perfil via GET /auth/me
                            profile_ok, profile_data = get_user_profile(token)
                            if profile_ok:
                                st.session_state.user_info = profile_data
                            
                            st.success("Login realizado com sucesso! Redirecionando...")
                            st.rerun()
                        else:
                            st.error(result)

    # --------------------------------------------------------------------------
    # Aba 2: Formulário de Cadastro (POST /auth/signup)
    # --------------------------------------------------------------------------
    with tab_signup:
        st.subheader("Criar Nova Conta no EduTrack AI")
        with st.form("form_signup"):
            signup_name = st.text_input("Nome Completo*", placeholder="Ex: Ana Silva")
            signup_email = st.text_input("E-mail Institucional ou Pessoal*", placeholder="exemplo@faculdadeimpacta.com.br")
            signup_pass = st.text_input("Senha*", type="password", placeholder="Mínimo de 6 caracteres")
            signup_pass_confirm = st.text_input("Confirmação de Senha*", type="password", placeholder="Repita sua senha")

            btn_signup = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

            if btn_signup:
                if not signup_name.strip():
                    st.warning("O campo Nome é obrigatório.")
                elif not signup_email.strip() or "@" not in signup_email:
                    st.warning("Informe um endereço de e-mail válido.")
                elif not signup_pass or len(signup_pass) < 6:
                    st.warning("A senha deve possuir pelo menos 6 caracteres.")
                elif signup_pass != signup_pass_confirm:
                    st.warning("As senhas informadas não coincidem.")
                else:
                    with st.spinner("Registrando sua conta..."):
                        success, result = signup_user(signup_name, signup_email, signup_pass)
                        if success:
                            token = result.get("authToken")
                            st.session_state.auth_token = token
                            
                            # Carrega os dados do perfil via GET /auth/me
                            profile_ok, profile_data = get_user_profile(token)
                            if profile_ok:
                                st.session_state.user_info = profile_data

                            st.success("Cadastro realizado com sucesso! Bem-vindo(a) ao EduTrack AI.")
                            st.rerun()
                        else:
                            st.error(result)
