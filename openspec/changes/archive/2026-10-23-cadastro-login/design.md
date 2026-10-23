## Context

O backend do EduTrack AI possui os endpoints de autenticação Xano já declarados em `api/authentication/auth/`:
- `POST /auth/login`: Recebe `email` e `password`, retornando `authToken` e `user_id`.
- `POST /auth/signup`: Recebe `name`, `email` e `password`, gravando no registro da tabela `user` e retornando `authToken` e `user_id`.
- `GET /auth/me`: Rota protegida por autenticação Bearer (`auth = "user"`), retornando os dados cadastrais do usuário (`id`, `name`, `email`, `role`, `created_at`).

No frontend em Streamlit, o arquivo `pages/3_👤_Perfil.py` está atualmente vazio. Esta especificação detalha como estruturar a interface de autenticação, o armazenamento de credenciais em sessão e a integração HTTP com o Xano. Veja `proposal.md` para a motivação e `specs/cadastro-login/spec.md` para os requisitos comportamentais.

## Goals / Non-Goals

**Goals:**
- Configurar a variável `XANO_AUTH_BASE_URL` no arquivo `.env` na raiz do projeto apontando para a base da API de autenticação do Xano (`https://x8ki-letl-twmt.n7.xano.io/api:72mncMCo`).
- Implementar em `pages/3_👤_Perfil.py` a interface reativa do Streamlit com:
  - Abas ("Entrar" e "Cadastrar-se") quando o usuário não estiver autenticado.
  - Painel com detalhes do perfil do usuário e botão de Logout quando o usuário estiver autenticado.
- Gerenciar o estado de autenticação via `st.session_state` (`auth_token` e `user_info`).
- Tratar exceções de rede e códigos de erro HTTP exibindo feedbacks amigáveis (`st.error`, `st.success`, `st.warning`).

**Non-Goals:**
- Não criar nem modificar endpoints de backend ou arquivos `.xs` (não solicitado).
- Não criar novas tabelas no banco de dados (a tabela `user` já existe).
- Não executar comandos de push, sincronização ou deploy para o Xano (REGRA Nº 2 do `AGENTS.md`).
- Não implementar suítes de testes automatizados ou arquivos de mock (REGRA Nº 1 do `AGENTS.md`).

## Decisions

### 1. Organização da Interface com Abas no Streamlit
- Quando `st.session_state.get("auth_token")` não estiver definido, o usuário verá duas abas (`st.tabs(["🔑 Login", "📝 Cadastro"])`).
- Ao submeter o formulário de login com sucesso, o `authToken` é gravado no `st.session_state` e um `st.rerun()` é disparado para exibir a tela de perfil.
- Ao submeter o cadastro com sucesso, o usuário é cadastrado, autenticado diretamente e a tela de perfil é renderizada.

### 2. Gerenciamento de Sessão com `st.session_state`
- `st.session_state["auth_token"]`: Armazena a string do JWT Bearer token retornado pelo Xano.
- `st.session_state["user_info"]`: Armazena o dicionário com os dados retornados por `GET auth/me`.
- Ação de Logout: Remove essas chaves do `st.session_state` e invoca `st.rerun()`.

### 3. Integração com a API via `requests` e `dotenv`
- Carregar variáveis usando `os.getenv("XANO_AUTH_BASE_URL")` com auxílio de `dotenv.load_dotenv()`.
- Criação de funções utilitárias encapsuladas para chamada aos endpoints:
  - `login_user(base_url, email, password)`
  - `signup_user(base_url, name, email, password)`
  - `get_user_profile(base_url, token)`
- Inclusão do header `Authorization: f"Bearer {token}"` na chamada para `/auth/me`.

## Risks / Trade-offs

- **[Persistência efêmera da sessão no Streamlit]** → *Mitigação*: Armazenar o token em `st.session_state` garante retenção durante a navegação entre páginas da mesma aba do navegador.
- **[URL base não configurada ou inacessível]** → *Mitigação*: Validar a presença de `XANO_AUTH_BASE_URL` no `.env` e exibir alerta explícito na tela caso a variável esteja vazia ou ausente.
- **[Falhas de requisição HTTP ou indisponibilidade de rede]** → *Mitigação*: Envolver chamadas em blocos `try/except requests.exceptions.RequestException` capturando mensagens de erro retornadas pela API do Xano.

## Migration Plan

1. Definir a variável `XANO_AUTH_BASE_URL` no `.env` na raiz do projeto.
2. Implementar a interface e fluxos em `pages/3_👤_Perfil.py`.
3. Validar a inicialização e os fluxos de login, cadastro, visualização de perfil e logout.
