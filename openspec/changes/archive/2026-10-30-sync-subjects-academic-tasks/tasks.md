## 1. Configuração de Ambiente e Camada de Serviço

- [x] 1.1 Configurar as variáveis de ambiente em `.env` e implementar o módulo de serviço `services/api_service.py` com funções para `GET/POST /subjects` e `GET/POST /academic_tasks` enviando o header `Authorization: Bearer <token_jwt>` com tratamento de loading, erros de rede e expiração de token (HTTP 401), verificando a importação do módulo.

## 2. Sincronização da Tela de Disciplinas

- [x] 2.1 Atualizar `pages/1_📚_Disciplinas.py` para mapear a leitura de `GET /subjects` populando o catálogo e conectar o formulário de adição para salvar diretamente no Xano via `POST /subjects`, incluindo feedback visual de loading e tratamento de expiração do token JWT, verificando a sintaxe e comportamento do arquivo.

## 3. Sincronização da Tela de Tarefas

- [x] 3.1 Implementar `pages/2_📝_Tarefas.py` para mapear a leitura de `GET /academic_tasks` populando as tarefas e conectar o formulário de adição garantindo que o campo `subject_id` referencie a disciplina selecionada a partir de `GET /subjects`, incluindo feedback visual de loading e tratamento de expiração do token JWT, verificando a sintaxe e comportamento do arquivo.
