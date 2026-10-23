## 1. Configuração de Ambiente

- [x] 1.1 Configurar a variável `XANO_AUTH_BASE_URL` no arquivo `.env` na raiz do projeto com a URL base dos endpoints de autenticação do Xano, verificando se o arquivo foi criado/atualizado corretamente.

## 2. Implementação da Página de Perfil e Autenticação (Streamlit)

- [x] 2.1 Implementar as funções utilitárias de comunicação HTTP com os endpoints `auth/login`, `auth/signup` e `auth/me` do Xano em `pages/3_👤_Perfil.py`, verificando o tratamento de erros e respostas.
- [x] 2.2 Criar a interface de formulários de Login e Cadastro em `pages/3_👤_Perfil.py` com persistência do token de autenticação em `st.session_state`, verificando o fluxo de envio dos dados para a tabela `user`.
- [x] 2.3 Implementar o painel de exibição das informações do usuário autenticado obtidas via `auth/me` e o botão de Logout para encerramento de sessão em `pages/3_👤_Perfil.py`, verificando a alternância entre os estados logado e deslogado.
