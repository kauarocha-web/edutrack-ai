## Why

O EduTrack AI atualmente dispõe dos endpoints de autenticação configurados no backend Xano (`auth/login`, `auth/signup` e `auth/me`), mas a interface de usuário em Streamlit carece de mecanismos para cadastro, autenticação e visualização das informações do perfil do usuário em `pages/3_👤_Perfil.py`. É essencial disponibilizar essa integração para permitir que estudantes e professores acessem a plataforma de forma segura e personalizada.

## What Changes

- Configuração de variável de ambiente no arquivo `.env` na raiz do projeto (`XANO_AUTH_BASE_URL`) contendo a URL base dos serviços de autenticação do Xano.
- Implementação completa da página `pages/3_👤_Perfil.py` com Streamlit:
  - Aba/Seção de Cadastro de novos usuários consumindo o endpoint `POST auth/signup` persistindo os dados na tabela `user`.
  - Aba/Seção de Login consumindo o endpoint `POST auth/login` e recebendo o token de autenticação (`authToken`).
  - Gerenciamento de sessão via `st.session_state` para reter o token e estado de autenticação entre navegações.
  - Exibição das informações do usuário autenticado consumindo o endpoint `GET auth/me`.
  - Mecanismo de Logout para limpar a sessão autenticada.

## Capabilities

### New Capabilities
- `cadastro-login`: Fluxo de cadastro, autenticação (login), consulta de perfil e encerramento de sessão na página de Perfil do Streamlit, comunicando-se com a API de autenticação do Xano.

### Modified Capabilities

## Impact

- **Frontend (Streamlit)**: Implementação do fluxo de usuário no arquivo `pages/3_👤_Perfil.py`.
- **Configuração**: Criação ou atualização do arquivo `.env` na raiz do projeto com `XANO_AUTH_BASE_URL`.
- **Dependências Python**: Utilização de `streamlit`, `requests` e `python-dotenv` para consumo das APIs REST e leitura de configurações de ambiente.
