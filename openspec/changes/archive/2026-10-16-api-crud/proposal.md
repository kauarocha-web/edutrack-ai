## Why

Atualmente, o EduTrack AI dispõe dos esquemas de banco de dados definidos para as entidades `subjects` e `academic_tasks`, mas carece de endpoints RESTful para que os usuários possam gerenciar seus dados. É necessário disponibilizar operações completas de CRUD (Create, Read, Update, Delete) com autenticação obrigatória e isolamento estrito, assegurando que cada usuário acerte e modifique unicamente seus próprios registros.

## What Changes

- Criação dos endpoints CRUD para a tabela `subjects` em `api/subjects/`:
  - `POST /subjects`: Cadastra uma nova disciplina vinculada ao `user_id` autenticado.
  - `GET /subjects`: Lista as disciplinas pertencentes exclusivamente ao usuário autenticado (`user_id == $auth.id`).
  - `GET /subjects/{id}`: Retorna os detalhes de uma disciplina específica do usuário autenticado.
  - `PATCH /subjects/{id}`: Atualiza os dados de uma disciplina existente do usuário autenticado.
  - `DELETE /subjects/{id}`: Remove uma disciplina pertencente ao usuário autenticado.
- Criação dos endpoints CRUD para a tabela `academic_tasks` em `api/academic_tasks/`:
  - `POST /academic_tasks`: Cadastra uma nova tarefa acadêmica vinculada ao `user_id` autenticado.
  - `GET /academic_tasks`: Lista as tarefas acadêmicas pertencentes exclusivamente ao usuário autenticado (`user_id == $auth.id`).
  - `GET /academic_tasks/{id}`: Retorna os detalhes de uma tarefa específica do usuário autenticado.
  - `PATCH /academic_tasks/{id}`: Atualiza os dados de uma tarefa existente do usuário autenticado.
  - `DELETE /academic_tasks/{id}`: Remove uma tarefa acadêmica pertencente ao usuário autenticado.
- Configuração de autenticação obrigatória (`auth = "user"`) e validação de propriedade (`where = user_id == $auth.id`) em todas as operações.

## Capabilities

### New Capabilities
- `api-crud`: Endpoints CRUD completos para as tabelas `subjects` e `academic_tasks` com controle de acesso e isolamento por usuário autenticado.

### Modified Capabilities
<!-- Nenhuma especificação existente teve seus requisitos alterados. -->

## Impact

- **APIs (Xano)**: Novos grupos e arquivos de endpoints em `api/subjects/` e `api/academic_tasks/`.
- **Segurança**: Isolamento multi-tenant garantido por meio do filtro obrigatório de autenticação `$auth.id`.
- **Dependências**: Integração direta com as tabelas existentes `table/subjects.xs`, `table/academic_tasks.xs` e `table/user.xs`.
