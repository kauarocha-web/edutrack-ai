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

## Especificações Arquivadas (`logica-calculo-progresso`)
- [x] Criação do script Python em `scripts/calculate_progress.py` com a função de cálculo de porcentagem de progresso por disciplina retornando JSON.
- [x] Integração aos endpoints CRUD de tarefas e disciplinas com suporte à autenticação Bearer token JWT e interface CLI.
- [x] Arquivamento no OpenSpec (`openspec/specs/logica-calculo-progresso/spec.md` promovido e mudança arquivada em `openspec/changes/archive/2026-10-30-logica-calculo-progresso`).

## Especificações Arquivadas (`api-crud`)
- [x] Implementação dos endpoints CRUD de `subjects` com filtro obrigatório por `user_id == $auth.id` em `api/subjects/`.
- [x] Implementação dos endpoints CRUD de `academic_tasks` com filtro obrigatório por `user_id == $auth.id` em `api/academic_tasks/`.
- [x] Arquivamento no OpenSpec (`openspec/specs/api-crud/spec.md` promovido e mudança arquivada).

## Especificações Arquivadas (`cadastro-login`)
- [x] Configuração da variável `XANO_AUTH_BASE_URL` no arquivo `.env` na raiz do projeto.
- [x] Implementação da página de Perfil com cadastro (`auth/signup`), login (`auth/login`), dados do perfil (`auth/me`) e logout em `pages/3_👤_Perfil.py`.
- [x] Arquivamento no OpenSpec (`openspec/specs/cadastro-login/spec.md` promovido e mudança arquivada em `openspec/changes/archive/2026-10-23-cadastro-login`).

## Especificações Arquivadas (`sync-subjects-academic-tasks`)
- [x] Configuração de `.env` e criação do serviço `services/api_service.py` com suporte aos endpoints `subjects` e `academic_tasks` via Bearer token JWT.
- [x] Atualização de `pages/1_📚_Disciplinas.py` conectando leitura (`GET /subjects`) e adição (`POST /subjects`) com feedback de loading e tratamento de erro/401.
- [x] Implementação de `pages/2_📝_Tarefas.py` conectando leitura (`GET /academic_tasks`), seleção de disciplina vinculada (`GET /subjects`) e criação (`POST /academic_tasks`) com `subject_id`, loading e tratamento de erro/401.
- [x] Arquivamento no OpenSpec (`openspec/specs/sync-subjects-academic-tasks/spec.md` promovido e mudança arquivada em `openspec/changes/archive/2026-10-30-sync-subjects-academic-tasks`).

## Especificações Arquivadas (`geracao-relatorio-pdf`)
- [x] Script Python `scripts/generate_report_pdf.py` para gerar relatório de desempenho do aluno em formato PDF com suporte CLI e modo autônomo.
- [x] Descritor de grupo `api/reports/reports.xs` e endpoint autenticado `GET /reports/performance` em `api/reports/reports_performance_GET.xs` no Xano para baixar o relatório.
- [x] Integração do download de PDF no frontend Streamlit (`pages/2_📝_Tarefas.py` e `app.py`).
- [x] Arquivamento no OpenSpec (`openspec/specs/geracao-relatorio-pdf/spec.md` promovido e mudança arquivada em `openspec/changes/archive/2026-11-09-geracao-relatorio-pdf`).

