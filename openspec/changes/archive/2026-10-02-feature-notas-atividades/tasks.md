## 1. Implementação do Lançamento de Notas

- [ ] 1.1 Criar tabela `activity_grades` no diretório `tables/` contendo os campos `id`, `created_at`, `task_id`, `student_id`, `user_id` (FK para `user`) e `grade`, verificando a conformidade da sintaxe XanoScript.
- [ ] 1.2 Criar API POST `/activity_grades` (para lançar nota) com autenticação do professor e validação dos campos obrigatórios, verificando a criação do arquivo de endpoint correspondente.
