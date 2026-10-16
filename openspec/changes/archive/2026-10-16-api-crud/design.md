## Context

O backend do EduTrack AI é modelado em XanoScript e estruturado para execução no Xano. As tabelas `subjects` e `academic_tasks` já possuem os schemas definidos em `table/` com o campo de relacionamento `user_id` vinculado à tabela de autenticação `user`. Para permitir o gerenciamento completo dessas entidades pela aplicação com segurança, planejamos a criação dos endpoints RESTful CRUD completos com isolamento rigoroso por usuário. Veja `proposal.md` para motivação e `specs/api-crud/spec.md` para os requisitos.

## Goals / Non-Goals

**Goals:**
- Projetar os endpoints CRUD para a tabela `subjects` em `api/subjects/`: `POST /subjects`, `GET /subjects`, `GET /subjects/{id}`, `PATCH /subjects/{id}` e `DELETE /subjects/{id}`.
- Projetar os endpoints CRUD para a tabela `academic_tasks` em `api/academic_tasks/`: `POST /academic_tasks`, `GET /academic_tasks`, `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}` e `DELETE /academic_tasks/{id}`.
- Exigir autenticação obrigatória (`auth = "user"`) em todos os endpoints.
- Aplicar o filtro obrigatório `$db.<tabela>.user_id == $auth.id` em todas as consultas e mutações para garantir que nenhum usuário visualize, modifique ou remova dados de terceiros.
- Atribuir o `user_id` dos novos registros diretamente a partir de `$auth.id`.

**Non-Goals:**
- Não criar suítes de testes automatizados ou arquivos de mock (fora do escopo solicitado).
- Não alterar código ou páginas do frontend Streamlit.
- Não executar comandos de push, sincronização ou deploy para o servidor remoto do Xano (REGRA Nº 2 do `AGENTS.md`).

## Decisions

### 1. Organização dos Grupos e Arquivos de API
- **Disciplinas**:
  - Grupo: `api/subjects/subjects.xs`
  - Rotas:
    - `POST /subjects`: Cria disciplina (`name`, `teacher`, `hours`) associando `user_id = $auth.id`.
    - `GET /subjects`: Lista disciplinas onde `user_id == $auth.id`.
    - `GET /subjects/{id}`: Retorna disciplina onde `id == $input.id` e `user_id == $auth.id` (retorna 404 se não pertencer).
    - `PATCH /subjects/{id}`: Atualiza campos da disciplina garantindo `user_id == $auth.id`.
    - `DELETE /subjects/{id}`: Remove a disciplina garantindo `user_id == $auth.id`.
- **Tarefas Acadêmicas**:
  - Grupo: `api/academic_tasks/academic_tasks.xs`
  - Rotas:
    - `POST /academic_tasks`: Cria tarefa acadêmica (`title`, `description`, `due_date`, `status`, `subject_id`) associando `user_id = $auth.id`.
    - `GET /academic_tasks`: Lista tarefas onde `user_id == $auth.id`.
    - `GET /academic_tasks/{id}`: Retorna tarefa onde `id == $input.id` e `user_id == $auth.id`.
    - `PATCH /academic_tasks/{id}`: Atualiza campos da tarefa validando `user_id == $auth.id`.
    - `DELETE /academic_tasks/{id}`: Remove tarefa validando `user_id == $auth.id`.

### 2. Padrão de Segurança Multi-Tenant (Prevenção de IDOR)
- Em nenhuma rota de criação o `user_id` será recebido no corpo da requisição (`$input`). O `user_id` será sempre extraído de forma segura do token autenticado (`$auth.id`).
- Em todas as operações de busca individual (`GET /{id}`), atualização (`PATCH /{id}`) e exclusão (`DELETE /{id}`), a condição de filtro no banco combinará `id == $input.id` com `user_id == $auth.id`.

## Risks / Trade-offs

- **[Vazamento de Dados por ID Inseguro (IDOR)]** → *Mitigação*: Todas as operações do XanoScript incluem expressamente o filtro `user_id == $auth.id` nas cláusulas `where` de `db.query`, `db.get`, `db.patch` e `db.delete`.
- **[Exclusão de Disciplinas com Tarefas Vinculadas]** → *Mitigação*: Tratamento no endpoint de exclusão de disciplina para lidar com dependências relacionais de tarefas.

## Migration Plan

1. Criar os descritores de grupo de API em `api/subjects/` e `api/academic_tasks/`.
2. Gerar os arquivos de rota XanoScript correspondentes aos endpoints CRUD.
3. Validar conformidade de especificações com `openspec validate api-crud`.
