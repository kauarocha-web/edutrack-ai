## Context

O backend Xano do EduTrack AI possui os endpoints RESTful já implementados:
- Grupo `Subjects` (`canonical = "4cvOQ4Zo"`): `GET /subjects` e `POST /subjects` (esperando `name`, `teacher`, `hours` e associando `user_id = $auth.id`).
- Grupo `Academic Tasks` (`canonical = "CwqMGDvq"`): `GET /academic_tasks` e `POST /academic_tasks` (esperando `title`, `description`, `due_date`, `status`, `subject_id` e associando `user_id = $auth.id`).

Ambos os grupos de API exigem autenticação obrigatória (`auth = "user"`), exigindo que o cabeçalho `Authorization: Bearer <token_jwt>` seja enviado em cada requisição. O token do usuário já é gerado e armazenado na sessão do Streamlit (`st.session_state["auth_token"]`) através do fluxo de login e cadastro em `pages/3_👤_Perfil.py`.

## Goals / Non-Goals

**Goals:**
- Criar a camada de serviço `services/api_service.py` para centralizar as chamadas HTTP para `subjects` e `academic_tasks`, encapsulando envio de headers, tratamento de erro de rede e detecção de status HTTP 401 (token expirado).
- Atualizar `.env` com as URLs base dos endpoints dos grupos `Subjects` e `Academic Tasks` do Xano.
- Atualizar `pages/1_📚_Disciplinas.py` para listar disciplinas via `GET /subjects` e cadastrar via `POST /subjects`, incluindo `st.spinner` durante o carregamento e mensagem de autenticação se deslogado.
- Atualizar `pages/2_📝_Tarefas.py` para listar tarefas via `GET /academic_tasks`, carregar disciplinas ativas para seleção de `subject_id` e cadastrar novas tarefas via `POST /academic_tasks`, incluindo indicadores visuais de loading.
- Exibir alertas claros quando a sessão expirar (401 Unauthorized), orientando o usuário a refazer o login na página de Perfil.

**Non-Goals:**
- Não criar nem modificar arquivos `.xs` de backend ou tabelas do banco de dados.
- Não executar comandos de push, sincronização ou deploy para o servidor remoto do Xano (REGRA Nº 2 do `AGENTS.md`).
- Não adicionar endpoints extras de consulta, exclusão ou edição nas telas que não foram solicitadas explicitamente (REGRA Nº 1 do `AGENTS.md`).

## Decisions

### 1. Camada de Serviço Centralizada (`services/api_service.py`)
- Funções dedicadas para os endpoints solicitados:
  - `get_subjects(token)`
  - `create_subject(token, name, teacher, hours)`
  - `get_academic_tasks(token)`
  - `create_academic_task(token, title, description, due_date, status, subject_id)`
- Função auxiliar `_make_request(method, url, token, json_data)` para padronizar cabeçalhos, timeouts, tratamento de `requests.exceptions.RequestException` e identificação de HTTP 401.

### 2. Configuração de Endpoints no `.env`
- Adicionar:
  - `XANO_SUBJECTS_BASE_URL=https://x8ki-letl-twmt.n7.xano.io/api:4cvOQ4Zo`
  - `XANO_TASKS_BASE_URL=https://x8ki-letl-twmt.n7.xano.io/api:CwqMGDvq`
- Se as variáveis não estiverem no `.env`, utilizar esses valores canônicos como fallback seguro.

### 3. Associação de `subject_id` em Tarefas
- Ao abrir a aba de criação de tarefas em `pages/2_📝_Tarefas.py`, as disciplinas do usuário autenticado são consultadas.
- O componente `st.selectbox` exibirá o nome da disciplina e armazenará seu respectivo `id` no payload enviado para `POST /academic_tasks`.

### 4. Gestão de Estados e Feedback Visual
- Uso de blocos `with st.spinner("Carregando...")` durante as requisições à API.
- Se `st.session_state.get("auth_token")` for nulo ou vazio, a tela exibe um aviso orientando o usuário a acessar a página de Perfil para realizar o login, impedindo disparos desnecessários à API.
- Quando o status retornado for 401, o serviço sinaliza expiração de token e a tela orienta a reautenticação.

## Risks / Trade-offs

- **[Usuário tenta cadastrar tarefa sem ter disciplinas cadastradas]** → *Mitigação*: Validar se a lista de disciplinas está vazia e alertar o usuário para criar primeiro uma disciplina antes de cadastrar uma tarefa vinculada.
- **[Token expirado durante uso da página]** → *Mitigação*: Detecção do status 401 e exibição de alerta amigável de sessão expirada.
- **[Conexão instável ou falha de rede]** → *Mitigação*: Timeout de 8 segundos com captura de `RequestException` e mensagens claras com `st.error`.

## Migration Plan

1. Configurar variáveis no arquivo `.env`.
2. Criar `services/api_service.py` com as funções de comunicação HTTP.
3. Atualizar `pages/1_📚_Disciplinas.py` integrando com `api_service`.
4. Atualizar `pages/2_📝_Tarefas.py` integrando com `api_service`.
5. Validar sintaxe e conformidade das páginas com o ambiente virtual.
