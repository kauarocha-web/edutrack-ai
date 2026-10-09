## Context

O backend do EduTrack AI utiliza XanoScript com entidades de banco modeladas no diretório `table/`. Atualmente, existem as tabelas `user`, `event_log` e `subjects`. Para possibilitar o controle de obrigações escolares, precisamos definir o modelo de dados para a entidade `academic_tasks`. Em estrito acordo com o `AGENTS.md`, o escopo é focado unicamente na modelagem da tabela, sem APIs CRUD ou testes automatizados. Veja `proposal.md` para motivação e `specs/academic-tasks/spec.md` para requisitos.

## Goals / Non-Goals

**Goals:**
- Definir o modelo de dados para a tabela `academic_tasks` em XanoScript (`table/academic_tasks.xs`).
- Estabelecer os campos solicitados: `title` (text), `description` (text), `due_date` (date), `status` (text) e `subject_id` (FK para `subjects`).
- Associar o vínculo obrigatório com o aluno autenticado (`user_id`, FK para `user`) conforme regras do `AGENTS.md`.
- Configurar índices primários e de busca.

**Non-Goals:**
- Não criar endpoints de API CRUD (como `GET /academic_tasks`, `POST /academic_tasks`, etc.) sem solicitação expressa do usuário.
- Não criar scripts de teste ou componentes de interface no Streamlit.
- Não executar comandos de push ou deploy remoto para o Xano.

## Decisions

### 1. Modelagem da Tabela `academic_tasks`
- **Arquivo**: `table/academic_tasks.xs`
- **Campos**:
  - `id`: `int` (chave primária)
  - `created_at`: `timestamp?=now` (registro de criação)
  - `title`: `text filters=trim` (título da obrigação acadêmica)
  - `description`: `text? filters=trim` (descrição detalhada / instruções)
  - `due_date`: `date?` (prazo limite de entrega)
  - `status`: `text?="pending" filters=trim` (status da tarefa, com default "pending")
  - `subject_id`: `int` com `{ table = "subjects" }` (referência relacional para a disciplina)
  - `user_id`: `int` com `{ table = "user" }` (referência relacional para o usuário autenticado)
- **Índices**:
  - Primary em `id`
  - Btree em `created_at` (ordem decrescente)
  - Btree em `subject_id` (ordem crescente)
  - Btree em `user_id` (ordem crescente)
  - Btree em `due_date` (ordem crescente)

## Risks / Trade-offs

- **[Integridade Referencial Cruzada]** → *Mitigação*: Uso de chaves estrangeiras explícitas (`subject_id` e `user_id`) assegura integridade relacional no banco Xano.

## Migration Plan

1. Definir o arquivo de esquema `table/academic_tasks.xs`.
2. Validar conformidade de artefatos com `openspec validate create-academic-tasks-table`.
