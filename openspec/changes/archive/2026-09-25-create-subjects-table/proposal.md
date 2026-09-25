## Why

O EduTrack AI precisa registrar componentes curriculares (disciplinas) no backend acadêmico. Esta alteração introduz o esquema da tabela `subjects` no XanoScript para armazenar as matérias, seus respectivos professores, carga horária e vinculação com os usuários da instituição.

## What Changes

- Definição do esquema da tabela `subjects` no arquivo `tables/subjects.xs`.
- Mapeamento dos seguintes campos:
  - `id`: identificador inteiro primário auto-incremental.
  - `name`: nome da disciplina (text).
  - `teacher`: nome do professor da matéria (text).
  - `hours`: carga horária da disciplina em horas (int).
  - `user_id`: chave estrangeira referenciando a tabela de autenticação `user` do Xano.
- Configuração dos índices de busca e ordenação (primary em `id`, btree em `created_at` e `user_id`).

## Capabilities

### New Capabilities
- `subjects`: Definição e armazenamento da entidade de disciplinas (`subjects`) associadas aos usuários no Xano.

### Modified Capabilities
<!-- Nenhuma especificação existente teve seus requisitos alterados. -->

## Impact

- **Banco de Dados (Xano)**: Novo arquivo de schema `tables/subjects.xs` com chave estrangeira apontando para a tabela `user`.
- **APIs e Testes**: Nenhum endpoint de CRUD ou teste adicionado nesta etapa, atendendo estritamente ao escopo definido no `AGENTS.md`.
