## 1. Configuração e Ajuste do Streamlit Secrets

- [x] 1.1 Corrigir a sintaxe do arquivo `.streamlit/secrets.toml` com as URLs base do Xano (`XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL`, `XANO_TASKS_BASE_URL`) em formato TOML válido e assegurar sua proteção no `.gitignore`, verificando o carregamento correto das chaves.

## 2. Migração da Leitura em Serviços e Páginas Streamlit

- [x] 2.1 Atualizar `services/api_service.py` para carregar as URLs do Xano a partir de `st.secrets` com fallback seguro para `os.environ` e valores padrão, verificando a resolução das URLs.
- [x] 2.2 Atualizar `pages/3_👤_Perfil.py` para obter `XANO_AUTH_BASE_URL` a partir de `st.secrets` em substituição à rotina manual de `.env`, verificando o carregamento da URL e os textos informativos da página.

