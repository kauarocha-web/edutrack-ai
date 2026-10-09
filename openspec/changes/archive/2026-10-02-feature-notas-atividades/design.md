## Context

O backend do EduTrack AI utiliza XanoScript e persistência no Xano. Conforme a REGRA Nº 1 do `AGENTS.md`, o escopo desta funcionalidade deve ater-se estritamente ao lançamento de notas solicitado pelo professor, sem a adição de consultas GET, exclusões ou CRUD completo. Veja `proposal.md` para motivação e `specs/activity-grades/spec.md` para os requisitos.

## Goals / Non-Goals

**Goals:**
- Modelar o schema da tabela `activity_grades` para armazenar as notas atribuídas pelos professores aos alunos em atividades específicas.
- Especificar o endpoint `POST /activity_grades` para o registro das notas.
- Garantir a integridade referencial vinculando o professor logado através do `user_id`.

**Non-Goals:**
- Não criar APIs de consulta (ex.: `GET /academic_tasks/{id}/grades` ou `GET /users/{id}/grades`), respeitando a regra de ouro do escopo do `AGENTS.md`.
- Não criar endpoints de atualização (PATCH/PUT) ou exclusão (DELETE) neste momento.
- Não incluir alterações no frontend Streamlit ou testes unitários sem solicitação explícita.
- Não realizar deploy ou push remoto para o Xano.

## Decisions

### 1. Estrutura da Tabela `activity_grades`
- **Tabela**: `activity_grades`
- **Campos**:
  - `id`: `int` (chave primária auto-incremental)
  - `created_at`: `timestamp?=now`
  - `task_id`: `int` (referência à atividade/tarefa acadêmica)
  - `student_id`: `int` com `{ table = "user" }` (referência ao aluno avaliado)
  - `user_id`: `int` com `{ table = "user" }` (referência ao professor autenticado)
  - `grade`: `decimal` (nota atribuída)
  - `feedback`: `text?` (comentário pedagógico opcional)
- **Índices**: Primário em `id`, índices btree em `task_id`, `student_id` e `user_id`.

### 2. Design do Endpoint `POST /activity_grades`
- **Rota**: `POST /activity_grades`
- **Entrada (Input)**: `task_id` (int), `student_id` (int), `grade` (decimal), `feedback?` (text).
- **Lógica**: Captura o `user_id` do token de autenticação do professor, valida os campos obrigatórios e insere o registro na tabela `activity_grades`.

## Risks / Trade-offs

- **[Integridade Referencial de Alunos e Tarefas]** → *Mitigação*: Validar a existência de `student_id` e `task_id` antes da inserção da nota.
