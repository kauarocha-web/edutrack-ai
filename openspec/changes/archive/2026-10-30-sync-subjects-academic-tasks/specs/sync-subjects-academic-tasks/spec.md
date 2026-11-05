# sync-subjects-academic-tasks Specification

## Purpose

Permite a sincronização completa das páginas de Disciplinas e Tarefas Acadêmicas do Streamlit com as APIs RESTful do Xano, consumindo os endpoints GET/POST de subjects e academic_tasks com o cabeçalho Authorization: Bearer <token_jwt>, feedback de loading e tratamento de expiração de sessão.

## ADDED Requirements

### Requirement: Autenticação Obrigatória nas Requisições aos Endpoints Xano
O sistema de serviço da aplicação SHALL incluir obrigatoriamente o cabeçalho HTTP `Authorization: Bearer <token_jwt>` em todas as requisições enviadas aos endpoints `GET /subjects`, `POST /subjects`, `GET /academic_tasks` e `POST /academic_tasks`.

#### Scenario: Requisição autenticada com token JWT válido
- **WHEN** uma requisição para a API de disciplinas ou tarefas for executada por um usuário logado
- **THEN** o sistema SHALL enviar o cabeçalho `Authorization: Bearer <token>` contendo o JWT do `st.session_state`

#### Scenario: Tentativa de acesso sem autenticação prévia
- **WHEN** o usuário acessa as páginas de Disciplinas ou Tarefas sem estar autenticado no sistema
- **THEN** o sistema SHALL alertar sobre a necessidade de login e bloquear chamadas à API remota

### Requirement: Sincronização da Tela de Disciplinas com a API
A tela de Disciplinas (`pages/1_📚_Disciplinas.py`) SHALL carregar e listar as disciplinas do usuário consumindo `GET /subjects` e permitir o cadastro de novas disciplinas via `POST /subjects` com envio direto ao Xano.

#### Scenario: Carregamento do catálogo de disciplinas
- **WHEN** o usuário autenticado acessa a página de Disciplinas
- **THEN** o sistema SHALL requisitar `GET /subjects` com feedback visual de carregamento e exibir as disciplinas retornadas

#### Scenario: Cadastro de nova disciplina com persistência no Xano
- **WHEN** o usuário preenche o formulário de cadastro de disciplina e clica em Salvar
- **THEN** o sistema SHALL enviar uma requisição `POST /subjects` contendo `name`, `teacher` e `hours`, exibir mensagem de sucesso e atualizar a listagem

### Requirement: Sincronização da Tela de Tarefas com a API e Vinculação de Disciplina
A tela de Tarefas (`pages/2_📝_Tarefas.py`) SHALL carregar as tarefas acadêmicas via `GET /academic_tasks` e permitir o cadastro de novas tarefas via `POST /academic_tasks`, garantindo que o campo `subject_id` referencie a disciplina selecionada pelo usuário.

#### Scenario: Carregamento das tarefas e lista de disciplinas para seleção
- **WHEN** o usuário autenticado acessa a página de Tarefas
- **THEN** o sistema SHALL requisitar `GET /academic_tasks` para listar as tarefas e `GET /subjects` para popular o seletor de disciplinas disponíveis

#### Scenario: Cadastro de nova tarefa acadêmica vinculada a uma disciplina
- **WHEN** o usuário preenche os dados da tarefa (título, descrição, prazo, status) selecionando uma disciplina válida e envia o formulário
- **THEN** o sistema SHALL enviar `POST /academic_tasks` associando o identificador `subject_id` da disciplina escolhida, exibir confirmação de sucesso e atualizar a lista de tarefas

### Requirement: Tratamento de Estados, Indicadores de Loading e Expiração de Token
O sistema SHALL fornecer feedback visual de progresso (loading) durante as requisições assíncronas e tratar respostas de erro da API, especialmente o código de status HTTP 401 (Unauthorized) referente a token JWT inválido ou expirado.

#### Scenario: Feedback visual durante o carregamento de dados
- **WHEN** qualquer operação de leitura ou criação for iniciada junto à API
- **THEN** o sistema SHALL exibir um indicador visual de loading (`st.spinner`) enquanto a resposta estiver pendente

#### Scenario: Detecção de token JWT expirado ou inválido (HTTP 401)
- **WHEN** o servidor Xano retornar o código HTTP 401 para uma requisição
- **THEN** o sistema SHALL exibir um alerta orientando o usuário de que sua sessão expirou e deve refazer o login na página de Perfil
