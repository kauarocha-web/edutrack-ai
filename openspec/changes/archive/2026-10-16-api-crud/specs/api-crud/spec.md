# api-crud Specification

## Purpose

Permite que usuários autenticados gerenciem completamente suas disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`) através de operações RESTful de CRUD, garantindo isolamento total para que cada usuário acesse e altere exclusivamente seus próprios dados.

## ADDED Requirements

### Requirement: CRUD de Disciplinas (Subjects) com Isolamento de Usuário
O sistema SHALL fornecer operações CRUD completas (`POST /subjects`, `GET /subjects`, `GET /subjects/{id}`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`) na tabela `subjects`, exigindo autenticação do usuário e assegurando que todas as leituras, modificações e exclusões filtrem estritamente por `user_id == $auth.id`.

#### Scenario: Criação de disciplina associada ao usuário autenticado
- **WHEN** um usuário autenticado envia uma requisição `POST /subjects` com dados válidos (`name`, `teacher`, `hours`)
- **THEN** o sistema SHALL salvar o registro associando automaticamente o `user_id` do usuário logado e retornar o registro criado

#### Scenario: Listagem de disciplinas restrita aos dados do usuário
- **WHEN** um usuário autenticado envia uma requisição `GET /subjects`
- **THEN** o sistema SHALL retornar apenas as disciplinas cadastradas pelo usuário autenticado (`user_id == $auth.id`)

#### Scenario: Consulta de disciplina por ID pertencente ao usuário
- **WHEN** um usuário autenticado envia `GET /subjects/{id}` para uma disciplina de sua propriedade
- **THEN** o sistema SHALL retornar os detalhes da disciplina solicitada

#### Scenario: Tentativa de consulta de disciplina de outro usuário
- **WHEN** um usuário autenticado tenta consultar via `GET /subjects/{id}` uma disciplina cujo `user_id` não seja o seu
- **THEN** o sistema SHALL retornar erro de não encontrado (404 Not Found)

#### Scenario: Atualização de disciplina do usuário autenticado
- **WHEN** um usuário autenticado envia `PATCH /subjects/{id}` com novos dados para sua disciplina
- **THEN** o sistema SHALL validar que `user_id == $auth.id`, atualizar os campos e retornar a disciplina modificada

#### Scenario: Exclusão de disciplina do usuário autenticado
- **WHEN** um usuário autenticado envia `DELETE /subjects/{id}` para uma disciplina de sua propriedade
- **THEN** o sistema SHALL remover o registro da base de dados e retornar confirmação de sucesso

### Requirement: CRUD de Tarefas Acadêmicas (Academic Tasks) com Isolamento de Usuário
O sistema SHALL fornecer operações CRUD completas (`POST /academic_tasks`, `GET /academic_tasks`, `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`) na tabela `academic_tasks`, exigindo autenticação do usuário e assegurando que todas as consultas e alterações afetem unicamente tarefas onde `user_id == $auth.id`.

#### Scenario: Criação de tarefa vinculada ao usuário autenticado
- **WHEN** um usuário autenticado envia `POST /academic_tasks` com `title`, `subject_id`, `due_date`, `status` e `description`
- **THEN** o sistema SHALL criar a tarefa acadêmica vinculando obrigatoriamente o `user_id` do usuário logado

#### Scenario: Listagem de tarefas acadêmicas do usuário
- **WHEN** um usuário autenticado envia `GET /academic_tasks`
- **THEN** o sistema SHALL retornar exclusivamente a lista de tarefas onde `user_id == $auth.id`

#### Scenario: Consulta de tarefa por ID pertencente ao usuário
- **WHEN** um usuário autenticado envia `GET /academic_tasks/{id}` para uma tarefa de sua propriedade
- **THEN** o sistema SHALL retornar os detalhes completos da tarefa solicitada

#### Scenario: Tentativa de consulta de tarefa de outro usuário
- **WHEN** um usuário autenticado tenta acessar `GET /academic_tasks/{id}` de uma tarefa pertencente a outro usuário
- **THEN** o sistema SHALL retornar erro 404 (Not Found)

#### Scenario: Atualização de tarefa do usuário autenticado
- **WHEN** um usuário autenticado envia `PATCH /academic_tasks/{id}` para uma tarefa de sua propriedade
- **THEN** o sistema SHALL aplicar as atualizações após validar `user_id == $auth.id` e retornar os dados atualizados

#### Scenario: Exclusão de tarefa do usuário autenticado
- **WHEN** um usuário autenticado envia `DELETE /academic_tasks/{id}` para uma tarefa de sua propriedade
- **THEN** o sistema SHALL excluir a tarefa do banco de dados e retornar mensagem de sucesso
