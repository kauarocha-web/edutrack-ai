## Context

O backend do EduTrack AI é modelado em XanoScript com persistência no Xano. Em conformidade com o `AGENTS.md`, o escopo desta alteração é estritamente limitado à modelagem de dados da tabela `subjects`, sem adição não solicitada de endpoints CRUD, testes unitários, sincronização de backend ou interface visual. Veja `proposal.md` para contexto e `specs/subjects/spec.md` para os requisitos.

## Goals / Non-Goals

**Goals:**
- Definir o arquivo de esquema `tables/subjects.xs` no formato XanoScript.
- Estruturar os campos solicitados: `id` (auto/int), `name` (text), `teacher` (text), `hours` (int) e `user_id` (FK para tabela `user`).
- Configurar chave primária em `id` e índices de ordenação e consulta em `created_at` e `user_id`.

**Non-Goals:**
- Não criar APIs ou rotas CRUD em `apis/` (vedado pelo `AGENTS.md` sem instrução explícita).
- Não criar rotinas de teste automatizado ou interface de usuário.
- Não executar operações de push, sync ou deploy para o Xano.

## Decisions

### 1. Modelagem da Tabela `subjects`
- **Arquivo**: `tables/subjects.xs`
- **Campos**:
  - `id`: `int` (chave primária auto-incremental)
  - `created_at`: `timestamp?=now` (data e hora de registro)
  - `name`: `text` (com filtro `trim`)
  - `teacher`: `text` (com filtro `trim`)
  - `hours`: `int` (carga horária da disciplina)
  - `user_id`: `int?` com bloco `{ table = "user" }` (referência à tabela de autenticação `user`)
- **Índices**:
  - `{type: "primary", field: [{name: "id"}]}`
  - `{type: "btree", field: [{name: "created_at", op: "desc"}]}`
  - `{type: "btree", field: [{name: "user_id", op: "asc"}]}`
- **Alternativas consideradas**:
  - `teacher_id`: Descartado em favor de `teacher (text)` e `user_id (FK para user)` para respeitar a estrutura exata solicitada pelo usuário.

## Risks / Trade-offs

- **[Integridade Referencial]** → *Mitigação*: `user_id` mapeia diretamente para a tabela de autenticação `user`, mantendo compatibilidade com o ecossistema nativo do Xano.

## Migration Plan

1. Criar o arquivo `tables/subjects.xs` no repositório.
2. Validar conformidade com `openspec validate`.
