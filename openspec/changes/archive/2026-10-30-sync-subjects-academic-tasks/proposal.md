## Why

Com a autenticação de usuários já disponível no EduTrack AI via token JWT, as telas de gerenciamento de Disciplinas e Tarefas Acadêmicas precisam ser conectadas diretamente à API do Xano. Atualmente, os componentes do Streamlit operam com dados simulados ou desacoplados, necessitando da integração com os endpoints REST de `subjects` e `academic_tasks` utilizando o header `Authorization: Bearer <token_jwt>`, feedback de carregamento e tratamento de expiração de token.

## What Changes

- Criação de um módulo central de serviço (`services/api_service.py`) para encapsular as requisições autenticadas aos endpoints de `subjects` e `academic_tasks` do Xano, incluindo validação e envio do header `Authorization: Bearer <token_jwt>`, tratamento de erros HTTP e detecção de expiração do token JWT (401 Unauthorized).
- Atualização da configuração em `.env` para garantir as URLs base dos grupos de API do Xano (`XANO_SUBJECTS_BASE_URL` e `XANO_TASKS_BASE_URL` ou base unificada).
- Atualização da tela de Disciplinas (`pages/1_📚_Disciplinas.py`):
  - Consulta à API (`GET /subjects`) com feedback visual de loading para popular o catálogo de disciplinas cadastradas.
  - Conexão do formulário de criação com `POST /subjects` para salvar registros diretamente no Xano com feedback de sucesso/erro.
- Atualização da tela de Tarefas (`pages/2_📝_Tarefas.py`):
  - Consulta à API (`GET /academic_tasks` e `GET /subjects`) para popular a listagem de tarefas e o seletor de disciplinas vinculadas.
  - Conexão do formulário de criação com `POST /academic_tasks`, associando obrigatoriamente o `subject_id` da disciplina escolhida.
- Tratamento de estados e exceções:
  - Adição de indicadores visuais de loading (`st.spinner`).
  - Tratamento de expiração de token (401), alertando o usuário para renovar a sessão na página de Perfil.

## Capabilities

### New Capabilities
- `sync-subjects-academic-tasks`: Sincronização e integração das páginas de Disciplinas e Tarefas do Streamlit com a API REST do Xano utilizando autenticação Bearer JWT, mapeamento relacional entre tarefas e disciplinas, indicadores visuais de carregamento e tratamento de expiração de token.

### Modified Capabilities

## Impact

- **Frontend (Streamlit)**:
  - Criação de `services/api_service.py` com funções de comunicação com a API.
  - Atualização de `pages/1_📚_Disciplinas.py` e implementação de `pages/2_📝_Tarefas.py`.
- **Configuração**: Adição das chaves de endpoint em `.env` se necessário.
- **Segurança**: Todas as chamadas a `subjects` e `academic_tasks` passam a injetar o token JWT armazenado em `st.session_state["auth_token"]`.
