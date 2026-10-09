## Why

Os alunos do EduTrack AI precisam de uma estrutura de dados dedicada para registrar e gerenciar suas obrigações acadêmicas (lições, provas, trabalhos) vinculadas a cada disciplina, viabilizando o controle de prazos e acompanhamento de status.

## What Changes

- Criação da tabela `academic_tasks` no XanoScript (`table/academic_tasks.xs`).
- Mapeamento dos seguintes campos:
  - `id`: identificador inteiro primário auto-incremental.
  - `created_at`: data e hora de registro (`timestamp?=now`).
  - `title`: título da atividade/obrigação (`text`).
  - `description`: descrição ou orientações da atividade (`text`).
  - `due_date`: data limite de entrega (`date`).
  - `status`: status atual da tarefa (`text`).
  - `subject_id`: chave estrangeira referenciando a tabela `subjects` (`int`).
  - `user_id`: chave estrangeira referenciando a tabela de autenticação `user` (`int`).
- Configuração de índices para otimização de consultas (primary em `id`, índices em `subject_id`, `user_id`, `due_date` e `created_at`).

## Capabilities

### New Capabilities
- `academic-tasks`: Estrutura de dados e esquema para a tabela de tarefas acadêmicas (`academic_tasks`) vinculadas a disciplinas e alunos.

### Modified Capabilities
<!-- Nenhuma especificação existente teve seus requisitos alterados. -->

## Impact

- **Banco de Dados (Xano)**: Novo arquivo de schema `table/academic_tasks.xs` com referências relacionais para `subjects` e `user`.
- **APIs e Interfaces**: Nenhuma API CRUD, teste ou interface visual é criada nesta etapa, em estrito cumprimento à Regra nº 1 do `AGENTS.md`.
