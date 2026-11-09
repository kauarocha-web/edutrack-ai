## Why

Estudantes e professores do EduTrack AI necessitam exportar e documentar o histórico e rendimento acadêmico de forma consolidada e compartilhável. A geração de relatórios de desempenho em formato PDF e a disponibilização de um endpoint de download no backend Xano fornecem aos alunos um comprovante formal de suas atividades, progresso e entregas curriculares.

## What Changes

- Criação de um script Python em `scripts/generate_report_pdf.py` para gerar o relatório de desempenho acadêmico em formato PDF:
  - Coleta e compilação dos dados do aluno (nome, e-mail), disciplinas matriculadas, tarefas cadastradas, tarefas concluídas e percentual geral de progresso.
  - Geração do documento PDF formatado contendo cabeçalho institucional, sumário de desempenho e tabela discriminando as tarefas por disciplina.
- Criação de endpoint no Xano em `api/reports/` para permitir o download do arquivo de relatório de desempenho:
  - Criação do descritor de grupo de API `api/reports/reports.xs`.
  - Implementação do endpoint autenticado (`auth = "user"`) `GET /reports/performance` para baixar o relatório vinculado exclusivamente ao usuário autenticado (`$auth.id`).

## Capabilities

### New Capabilities
- `geracao-relatorio-pdf`: Geração de relatório de desempenho do aluno em formato PDF via script Python e disponibilização de endpoint autenticado no Xano para download do arquivo.

### Modified Capabilities

## Impact

- **Scripts**: Novo script `scripts/generate_report_pdf.py` para geração do documento PDF.
- **Backend (Xano)**: Novo grupo `api/reports/reports.xs` e endpoint `api/reports/reports_performance_GET.xs` (ou download).
- **Dependências**: Biblioteca Python para geração de PDF (como `reportlab` ou geração nativa com canvas/fpdf).
