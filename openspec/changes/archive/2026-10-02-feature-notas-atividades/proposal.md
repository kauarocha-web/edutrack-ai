## Why

Os professores do EduTrack AI necessitam de um mecanismo para registrar avaliações e notas atribuídas aos alunos em atividades acadêmicas específicas, viabilizando o acompanhamento pedagógico do desempenho individual no Innovation Lab.

## What Changes

- Criação da tabela `activity_grades` no XanoScript para registrar notas dos alunos por atividade.
- Implementação do endpoint `POST /activity_grades` permitindo ao professor lançar notas para os alunos em atividades específicas com validação do usuário logado.

## Capabilities

### New Capabilities
- `activity-grades`: Registro e lançamento de notas de alunos em atividades acadêmicas específicas por professores.

### Modified Capabilities
<!-- Nenhuma especificação existente teve seus requisitos alterados. -->

## Impact

- **Banco de Dados (Xano)**: Nova tabela `activity_grades` no diretório `tables/` vinculando aluno (`student_id`), atividade (`task_id`), nota (`grade`) e professor (`user_id`).
- **APIs (Xano)**: Novo endpoint `POST /activity_grades`.
- **Dependências / Sistemas**: Sem alterações que quebrem contratos existentes.
