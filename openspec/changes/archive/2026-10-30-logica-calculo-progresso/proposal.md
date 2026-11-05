## Why

No EduTrack AI, estudantes e professores necessitam mensurar o progresso acadêmico em cada disciplina com base nas atividades concluídas. Atualmente, o sistema carece de uma função dedicada em Python capaz de consolidar tarefas vinculadas a uma disciplina consumindo os endpoints CRUD e calcular a porcentagem de conclusão (`concluídas / total * 100`), estruturando a resposta em formato JSON.

## What Changes

- Criação do script Python em `scripts/calculate_progress.py`.
- Implementação de função que recebe o identificador da disciplina (`subject_id`) e o token de autenticação JWT, consome os endpoints CRUD (`GET /academic_tasks` e `GET /subjects`) e filtra as tarefas da respectiva disciplina.
- Cálculo da métrica de progresso: proporção de tarefas concluídas em relação ao total (`concluídas / total`), com tratamento seguro contra divisão por zero quando a disciplina não possuir tarefas (retornando 0.0% ou 0 tarefas).
- Formatação e retorno dos resultados em formato JSON estruturado, incluindo `subject_id`, total de tarefas, tarefas concluídas, tarefas pendentes e percentual de progresso formatado.

## Capabilities

### New Capabilities
- `logica-calculo-progresso`: Cálculo automatizado da porcentagem de progresso acadêmico por disciplina baseado nas tarefas concluídas vs total via endpoints CRUD, com retorno padronizado em JSON.

### Modified Capabilities

## Impact

- **Scripts**: Criação do diretório `scripts/` e do script `scripts/calculate_progress.py`.
- **APIs**: Consumo autenticado dos endpoints CRUD `GET /subjects` e `GET /academic_tasks`.
- **Dependências**: Reutilização de `requests` e `json` da biblioteca padrão do Python.
