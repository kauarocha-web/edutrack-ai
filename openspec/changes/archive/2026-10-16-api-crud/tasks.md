## 1. Endpoints CRUD de Subjects

- [x] 1.1 Criar o descritor de grupo `api/subjects/subjects.xs` e o endpoint `POST /subjects` persistindo a disciplina vinculada ao `user_id` do usuário autenticado (`$auth.id`), verificando a sintaxe do arquivo XanoScript gerado.
- [x] 1.2 Implementar os endpoints `GET /subjects` (listagem) e `GET /subjects/{id}` (detalhe) filtrando exclusivamente registros onde `user_id == $auth.id`, verificando os arquivos XanoScript criados.
- [x] 1.3 Implementar os endpoints `PATCH /subjects/{id}` (atualização) e `DELETE /subjects/{id}` (remoção) com verificação de propriedade por `$auth.id`, verificando os arquivos XanoScript criados.

## 2. Endpoints CRUD de Academic Tasks

- [x] 2.1 Criar o descritor de grupo `api/academic_tasks/academic_tasks.xs` e o endpoint `POST /academic_tasks` persistindo a tarefa vinculada ao `user_id` do usuário autenticado (`$auth.id`), verificando a sintaxe do arquivo XanoScript gerado.
- [x] 2.2 Implementar os endpoints `GET /academic_tasks` (listagem) e `GET /academic_tasks/{id}` (detalhe) filtrando exclusivamente registros onde `user_id == $auth.id`, verificando os arquivos XanoScript criados.
- [x] 2.3 Implementar os endpoints `PATCH /academic_tasks/{id}` (atualização) e `DELETE /academic_tasks/{id}` (remoção) com verificação de propriedade por `$auth.id`, verificando os arquivos XanoScript criados.
