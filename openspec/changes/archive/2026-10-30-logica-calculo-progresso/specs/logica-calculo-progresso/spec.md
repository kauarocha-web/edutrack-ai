# logica-calculo-progresso Specification

## Purpose

Define a lógica para cálculo de progresso acadêmico de disciplinas em Python, consumindo as tarefas via endpoints CRUD da plataforma e retornando uma estrutura JSON com contadores de tarefas e porcentagem de conclusão.

## ADDED Requirements

### Requirement: Cálculo da Porcentagem de Progresso de uma Disciplina
O script `scripts/calculate_progress.py` SHALL fornecer uma função que calcula a porcentagem de progresso de uma disciplina específica a partir de suas tarefas acadêmicas, computando a razão entre tarefas concluídas e o total de tarefas vinculadas (`concluídas / total * 100`).

#### Scenario: Disciplina com tarefas pendentes e concluídas
- **WHEN** a função de cálculo for executada para uma disciplina contendo 4 tarefas totais sendo 2 com status concluído (`status == "completed"`)
- **THEN** o sistema SHALL computar exatamente 50.0% de progresso

#### Scenario: Disciplina com todas as tarefas concluídas
- **WHEN** todas as tarefas associadas à disciplina estiverem com o status concluído
- **THEN** o sistema SHALL retornar 100.0% de progresso

#### Scenario: Disciplina sem nenhuma tarefa cadastrada
- **WHEN** uma disciplina não possuir nenhuma tarefa associada (total = 0)
- **THEN** o sistema SHALL tratar o caso sem erro de divisão por zero e retornar 0.0% de progresso

### Requirement: Consumo de Tarefas e Disciplinas via Endpoints CRUD
A lógica de cálculo SHALL utilizar os endpoints CRUD (`GET /academic_tasks` e `GET /subjects`) com o token JWT de autenticação para recuperar a lista oficial de tarefas pertencentes ao usuário autenticado.

#### Scenario: Obtenção de tarefas através da API REST
- **WHEN** o identificador da disciplina e o token JWT forem fornecidos
- **THEN** o sistema SHALL consultar as tarefas do usuário autenticado e filtrar apenas os registros onde `subject_id` corresponda à disciplina informada

#### Scenario: Disciplina inexistente ou inacessível
- **WHEN** for solicitado o cálculo para um `subject_id` inexistente ou pertencente a outro usuário
- **THEN** o sistema SHALL indicar erro na consulta ou retornar JSON de erro informativo

### Requirement: Retorno Estruturado em Formato JSON
O script SHALL estruturar e retornar o resultado do cálculo em formato JSON padronizado, contendo os campos: `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks`, `progress_percentage` e data/hora do cálculo.

#### Scenario: Formato e campos do JSON de saída
- **WHEN** o cálculo de progresso for finalizado com sucesso
- **THEN** o sistema SHALL retornar uma string ou dicionário JSON válido contendo `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks` e `progress_percentage`

#### Scenario: Execução do script via linha de comando (CLI)
- **WHEN** o script `scripts/calculate_progress.py` for executado diretamente no terminal informando os parâmetros necessários
- **THEN** o sistema SHALL imprimir no stdout o JSON com o resultado do cálculo
