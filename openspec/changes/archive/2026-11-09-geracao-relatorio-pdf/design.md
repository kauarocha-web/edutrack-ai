## Context

O EduTrack AI já possui tabelas e endpoints CRUD operacionais para disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`), além do cálculo de progresso implementado em `scripts/calculate_progress.py`. Os estudantes e professores necessitam de uma forma consolidada de visualizar, documentar e exportar o desempenho acadêmico em formato padronizado. Para atender a essa necessidade, planeja-se a criação de um script em Python dedicado à geração de relatórios em formato PDF e a especificação de um endpoint autenticado no Xano para download das informações consolidadas do relatório. Consulte `proposal.md` para a motivação e `specs/geracao-relatorio-pdf/spec.md` para os requisitos formais.

## Goals / Non-Goals

**Goals:**
- Criar o script Python `scripts/generate_report_pdf.py` para gerar o relatório de desempenho acadêmico em formato PDF (utilizando ReportLab com fallback resiliente para ambiente local).
- Desenhar a estrutura do relatório contendo:
  - Identificação do aluno e data de emissão.
  - Tabela consolidada com disciplinas, total de tarefas, tarefas concluídas e progresso percentual.
  - Listagem das tarefas acadêmicas com seus respectivos prazos e status.
- Criar a especificação do grupo de API `api/reports/reports.xs` e do endpoint autenticado `GET /reports/performance` em `api/reports/reports_performance_GET.xs` no Xano, assegurando autenticação Bearer token e filtro restrito por `$auth.id`.

**Non-Goals:**
- Não criar endpoints adicionais além do endpoint de download/dados do relatório solicitado (REGRA Nº 1 do `AGENTS.md`).
- Não modificar telas do frontend Streamlit neste momento (REGRA Nº 1 do `AGENTS.md`).
- Não executar comandos de push, sincronização ou deploy para o Xano (REGRA Nº 2 do `AGENTS.md`).

## Decisions

### 1. Biblioteca para Geração de PDF em Python
- Utilizar `reportlab` no ambiente virtual Python.
- O script incluirá tratamento resiliente de `sys.path` para detectar o `.venv/Lib/site-packages` (mesmo padrão adotado em `scripts/calculate_progress.py`), permitindo execução direta tanto pelo interpretador virtual quanto pelo comando padrão do sistema (`python scripts/generate_report_pdf.py`).
- Implementar suporte a execução autônoma (modo demonstração) quando executado sem token, além de integração com os dados do usuário quando fornecido token JWT.

### 2. Estrutura do Endpoint no Xano (`api/reports/`)
- Grupo: `Reports` (`api/reports/reports.xs`).
- Endpoint: `GET /reports/performance` (`api/reports/reports_performance_GET.xs`) com `auth = "user"`.
- O endpoint consulta as disciplinas e tarefas do usuário autenticado (`$auth.id`) e retorna o payload com os dados consolidados do estudante para o relatório.

## Risks / Trade-offs

- **[Dependência de pacote externo ReportLab]** → *Mitigação*: Verificar a instalação no `.venv` durante o apply e instalar via pip caso ausente.
- **[Filtragem de dados multi-usuário]** → *Mitigação*: Todas as consultas no endpoint Xano são restritas a `where = $db.*.user_id == $auth.id`.

## Migration Plan

1. Definir e validar a proposta e os requisitos no OpenSpec.
2. Na etapa de implementação (`apply`):
   - Criar `scripts/generate_report_pdf.py`.
   - Criar os arquivos XanoScript `api/reports/reports.xs` e `api/reports/reports_performance_GET.xs`.
   - Validar a geração do PDF localmente no terminal.
