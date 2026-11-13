## Why

Atualmente, as URLs base dos endpoints do backend Xano (`XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL` e `XANO_TASKS_BASE_URL`) são lidas a partir do arquivo `.env` usando funções customizadas de parsing e `python-dotenv`. O Streamlit possui um mecanismo nativo e seguro de gerenciamento de configurações e credenciais sensíveis através do `st.secrets` (armazenadas em `.streamlit/secrets.toml`), que é o padrão recomendado pela plataforma para desenvolvimento local e deploy no Streamlit Community Cloud. A migração da leitura do `.env` para o `st.secrets` simplifica o carregamento de configurações, elimina redundância de código de parsing e alinha a arquitetura às boas práticas do ecossistema Streamlit.

## What Changes

- Padronização e correção do arquivo de segredos locais em `.streamlit/secrets.toml`, configurando corretamente as variáveis `XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL` e `XANO_TASKS_BASE_URL`.
- Atualização do serviço de integração em `services/api_service.py` para obter as URLs do Xano prioritariamente via `st.secrets`, mantendo compatibilidade resiliente com `os.environ` ou defaults para execuções fora do contexto do Streamlit (como testes e scripts CLI).
- Atualização da página de autenticação e perfil em `pages/3_👤_Perfil.py` para carregar `XANO_AUTH_BASE_URL` a partir de `st.secrets` (com fallback gracioso), substituindo a função legada de carregamento manual de `.env`.
- Atualização dos textos informativos da interface de usuário que faziam referência ao `.env`, passando a indicar o uso de `secrets.toml`.

## Capabilities

### New Capabilities
- `migracao-env-para-secrets`: Leitura das configurações e URLs das APIs do Xano através de Streamlit secrets (st.secrets / .streamlit/secrets.toml) em substituição à leitura manual do arquivo .env.

### Modified Capabilities

## Impact

- **Frontend / Serviços**: `services/api_service.py` e `pages/3_👤_Perfil.py` passam a consumir as URLs do Xano a partir de `st.secrets`.
- **Configuração**: Validação do `.streamlit/secrets.toml` com sintaxe TOML válida e preservação no `.gitignore`.
- **Scripts Autônomos**: `scripts/calculate_progress.py` e `scripts/generate_report_pdf.py` permanecem compatíveis através de fallbacks transparentes.
