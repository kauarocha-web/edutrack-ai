# migracao-env-para-secrets Specification

## Purpose

Definir os requisitos para a migração da leitura das variáveis de ambiente e URLs das APIs do Xano do arquivo legado `.env` para o mecanismo nativo de segredos do Streamlit (`st.secrets` / `.streamlit/secrets.toml`), garantindo carregamento seguro, padronizado e com fallback para execução autônoma.

## ADDED Requirements

### Requirement: Configuração das URLs do Xano no Streamlit Secrets
As variáveis de conexão do backend Xano (`XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL` e `XANO_TASKS_BASE_URL`) SHALL ser configuradas no arquivo `.streamlit/secrets.toml` com sintaxe TOML válida, e este arquivo SHALL permanecer ignorado pelo controle de versão Git (`.gitignore`).

#### Scenario: Leitura de chaves a partir do secrets.toml
- **WHEN** a aplicação Streamlit é executada em ambiente local ou na nuvem
- **THEN** o sistema SHALL disponibilizar as chaves `XANO_AUTH_BASE_URL`, `XANO_SUBJECTS_BASE_URL` e `XANO_TASKS_BASE_URL` via dicionário `st.secrets`

#### Scenario: Proteção contra versionamento de credenciais
- **WHEN** arquivos novos ou modificados forem verificados no Git
- **THEN** o arquivo `.streamlit/secrets.toml` SHALL ser ignorado pelo `.gitignore`

### Requirement: Consumo de Secrets no Módulo de Serviços (api_service.py)
O módulo `services/api_service.py` SHALL obter as URLs base das APIs de Disciplinas (`XANO_SUBJECTS_BASE_URL`) e Tarefas (`XANO_TASKS_BASE_URL`) prioritariamente através de `st.secrets`, mantendo fallback para `os.environ` e URLs padrão caso a biblioteca Streamlit não esteja em execução com secrets carregados.

#### Scenario: Execução em contexto do Streamlit com secrets definidos
- **WHEN** uma requisição de API for iniciada a partir de uma página Streamlit que possui as chaves em `st.secrets`
- **THEN** o sistema SHALL utilizar as URLs configuradas em `st.secrets["XANO_SUBJECTS_BASE_URL"]` e `st.secrets["XANO_TASKS_BASE_URL"]`

#### Scenario: Execução isolada em linha de comando (scripts/CLI)
- **WHEN** funções de `services/api_service.py` forem importadas em scripts CLI sem inicialização de servidor Streamlit
- **THEN** o sistema SHALL aplicar o fallback gracioso para variáveis de ambiente ou URLs padrão canônicas sem levantar exceções não tratadas

### Requirement: Consumo de Secrets na Página de Perfil (pages/3_👤_Perfil.py)
A página `pages/3_👤_Perfil.py` SHALL obter a URL base de autenticação `XANO_AUTH_BASE_URL` a partir de `st.secrets`, dispensando a rotina de leitura manual de `.env` e atualizando os indicativos visuais para o usuário.

#### Scenario: Carregamento da URL de autenticação na página de perfil
- **WHEN** o usuário acessa a página de Perfil e Autenticação
- **THEN** o sistema SHALL carregar `XANO_AUTH_BASE_URL` de `st.secrets` e utilizar essa rota para operações de cadastro, login e verificação de perfil

#### Scenario: Visualização informativa na interface
- **WHEN** as informações de conexão do backend forem exibidas na página de Perfil
- **THEN** o sistema SHALL referenciar o `st.secrets` como fonte oficial de configuração
