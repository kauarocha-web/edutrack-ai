# academic-tasks Specification

## Purpose
Permite a estruturação, persistência e integridade das tarefas e obrigações acadêmicas (`academic_tasks`) vinculadas a disciplinas e alunos no EduTrack AI.

## Requirements

### Requirement: Tabela de Tarefas Acadêmicas
O sistema SHALL manter a tabela `academic_tasks` em XanoScript contendo os campos: identificador primário `id`, data de criação `created_at`, título `title` (text), descrição `description` (text), data limite `due_date` (date), situação `status` (text), referência à disciplina `subject_id` (FK para `subjects`) e referência ao aluno `user_id` (FK para `user`).

#### Scenario: Validação do esquema da tabela
- **WHEN** o esquema da tabela `academic_tasks` for inspecionado em `table/academic_tasks.xs`
- **THEN** o sistema SHALL conter os campos `id`, `created_at`, `title`, `description`, `due_date`, `status`, `subject_id` e `user_id` com a tipagem e filtros corretos

#### Scenario: Relacionamento com disciplina e aluno
- **WHEN** um registro de tarefa acadêmica for persistido com `subject_id` e `user_id`
- **THEN** o sistema SHALL validar que `subject_id` referencia a tabela `subjects` e `user_id` referencia a tabela de autenticação `user`
