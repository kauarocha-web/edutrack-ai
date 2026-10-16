# EduTrack AI - Tarefas do Projeto

## Tarefas Solicitadas (`create-subjects-table`)
- [x] Definição do esquema da tabela `subjects` em `tables/subjects.xs` (`id`, `name`, `teacher`, `hours`, `user_id` FK para `user`).
- [x] Arquivamento no OpenSpec (`openspec/specs/subjects/spec.md` promovido e mudança arquivada).

## Especificações Arquivadas (`feature-notas-atividades`)
- [x] Especificação promovida para `openspec/specs/activity-grades/spec.md`.
- [x] Mudança arquivada em `openspec/changes/archive/2026-10-02-feature-notas-atividades`.

## Especificações Arquivadas (`create-academic-tasks-table`)
- [x] Definição do esquema da tabela `academic_tasks` em `table/academic_tasks.xs` (`id`, `created_at`, `title`, `description`, `due_date`, `status`, `subject_id` FK para `subjects`, `user_id` FK para `user`).
- [x] Arquivamento no OpenSpec (`openspec/specs/academic-tasks/spec.md` promovido e mudança arquivada).

## Planejamento em Aberto (`logica-calculo-progresso`)
- [ ] Criar o script Python em `scripts/calculate_progress.py` com a função de cálculo de progresso por disciplina retornando JSON.

## Especificações Arquivadas (`api-crud`)
- [x] Implementação dos endpoints CRUD de `subjects` com filtro obrigatório por `user_id == $auth.id` em `api/subjects/`.
- [x] Implementação dos endpoints CRUD de `academic_tasks` com filtro obrigatório por `user_id == $auth.id` em `api/academic_tasks/`.
- [x] Arquivamento no OpenSpec (`openspec/specs/api-crud/spec.md` promovido e mudança arquivada).
