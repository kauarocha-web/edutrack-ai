# geracao-relatorio-pdf Specification

## Purpose
Definir a especificação técnica para a geração de relatórios de desempenho acadêmico em formato PDF através de um script Python e a disponibilização de um endpoint autenticado no backend Xano para download do arquivo de desempenho do aluno.

## Requirements

### Requirement: Script Python para Geração do Relatório de Desempenho em PDF
O sistema SHALL disponibilizar um script em `scripts/generate_report_pdf.py` capaz de compilar as informações acadêmicas do estudante (disciplinas, tarefas cadastradas, status de conclusão e porcentagem de progresso) e produzir um arquivo de documento no formato PDF com o desempenho consolidado.

#### Scenario: Geração do arquivo PDF de desempenho com sucesso
- **WHEN** o script `scripts/generate_report_pdf.py` for executado informando o caminho do arquivo de saída ou parâmetros do estudante
- **THEN** o sistema SHALL gerar um arquivo `.pdf` válido contendo cabeçalho institucional, dados das disciplinas e tarefas com suas respectivas situações de progresso

#### Scenario: Execução com dados em memória ou fallback demonstrativo
- **WHEN** o script for executado sem parâmetros de conexão de rede ou sem dados externos
- **THEN** o sistema SHALL utilizar dados estruturados padrão para gerar o PDF de demonstração sem erros de execução

### Requirement: Endpoint no Xano para Download do Relatório de Desempenho
O backend Xano SHALL fornecer um endpoint autenticado (`auth = "user"`) `GET /reports/performance` no grupo de API `Reports` para disponibilizar o relatório de desempenho acadêmico do usuário logado.

#### Scenario: Requisição autenticada de download do relatório
- **WHEN** um usuário autenticado enviar uma requisição `GET /reports/performance` com Bearer token JWT válido
- **THEN** o sistema SHALL responder com os dados consolidados do relatório de desempenho do estudante filtrados estritamente pelo `$auth.id`

#### Scenario: Tentativa de download sem autenticação
- **WHEN** uma requisição for realizada sem o cabeçalho `Authorization: Bearer <token>`
- **THEN** o sistema SHALL recusar o acesso com código de status HTTP `401 Unauthorized`
