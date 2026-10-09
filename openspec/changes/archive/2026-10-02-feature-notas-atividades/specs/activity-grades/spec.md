# activity-grades Specification

## Purpose

Permite que professores lancem e registrem notas de alunos em atividades acadêmicas específicas no EduTrack AI.

## ADDED Requirements

### Requirement: Tabela de Notas de Atividades
O sistema SHALL manter a tabela `activity_grades` para registrar avaliações contendo os campos: identificador primário `id`, referência à atividade (`task_id`), referência ao aluno (`student_id`), referência ao professor autenticado (`user_id`), valor da nota (`grade`) e data de registro (`created_at`).

#### Scenario: Estrutura da tabela de notas
- **WHEN** a tabela `activity_grades` for consultada no schema do Xano
- **THEN** o sistema SHALL conter os campos `id`, `task_id`, `student_id`, `user_id`, `grade` e `created_at` com as relações devidamente configuradas

### Requirement: Lançar Nota de Atividade
O sistema SHALL fornecer um endpoint `POST /activity_grades` para permitir que o professor autenticado lance a nota de um aluno em uma atividade específica.

#### Scenario: Lançamento de nota com sucesso
- **WHEN** um professor autenticado envia uma requisição `POST /activity_grades` com `task_id`, `student_id` e `grade` válidos
- **THEN** o sistema SHALL persistir a nota associada ao `user_id` autenticado e retornar o registro criado com status de sucesso

#### Scenario: Rejeição por falta de campos obrigatórios
- **WHEN** uma requisição `POST /activity_grades` é enviada sem os parâmetros obrigatórios `task_id`, `student_id` ou `grade`
- **THEN** o sistema SHALL rejeitar a requisição com mensagem de erro de validação
