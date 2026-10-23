# cadastro-login Specification

## Purpose
Permite que novos usuários realizem cadastro, usuários existentes realizem login e consultem os dados de sua conta na página de Perfil do EduTrack AI, integrando com as APIs de autenticação do Xano e armazenando a URL base no arquivo de ambiente `.env`.

## Requirements

### Requirement: Cadastro de Novo Usuário
O sistema Streamlit SHALL fornecer um formulário de cadastro que coleta nome (`name`), e-mail (`email`) e senha (`password`), enviando uma requisição `POST auth/signup` para o backend Xano para salvar os dados na tabela `user` e receber o token de autenticação.

#### Scenario: Cadastro realizado com sucesso
- **WHEN** o usuário preenche nome, e-mail e senha válidos e aciona o botão de cadastro
- **THEN** o sistema SHALL enviar a requisição `POST auth/signup`, salvar a sessão com o token retornado e exibir mensagem de boas-vindas com o perfil carregado

#### Scenario: Tentativa de cadastro com dados inválidos ou já existentes
- **WHEN** o usuário submete o formulário com campos em branco ou um e-mail já cadastrado
- **THEN** o sistema SHALL exibir uma mensagem de erro compreensível sem persistir a sessão

### Requirement: Autenticação de Usuário (Login)
O sistema Streamlit SHALL disponibilizar um formulário de login solicitando e-mail (`email`) e senha (`password`), submetendo uma requisição `POST auth/login` para o backend Xano e persistindo o token retornado na sessão do Streamlit (`st.session_state`).

#### Scenario: Login com credenciais válidas
- **WHEN** o usuário informa seu e-mail e senha cadastrados e clica em Entrar
- **THEN** o sistema SHALL autenticar contra o endpoint `POST auth/login`, salvar o `authToken` em `st.session_state` e carregar a visão autenticada do perfil

#### Scenario: Falha de autenticação por credenciais incorretas
- **WHEN** o usuário informa credenciais inválidas
- **THEN** o sistema SHALL exibir um alerta de erro de autenticação e manter a tela de login

### Requirement: Consulta de Dados do Usuário Autenticado (Auth Me)
O sistema SHALL consumir o endpoint `GET auth/me` enviando o token JWT obtido no cabeçalho `Authorization: Bearer <token>` para carregar e exibir as informações do usuário logado (nome, e-mail, papel e data de criação).

#### Scenario: Exibição das informações do usuário logado
- **WHEN** houver um token válido em `st.session_state`
- **THEN** o sistema SHALL consultar `GET auth/me` e renderizar as informações do usuário na página de Perfil

#### Scenario: Acesso à página sem usuário autenticado
- **WHEN** a página de Perfil for acessada sem nenhum token ativo em `st.session_state`
- **THEN** o sistema SHALL apresentar as opções de formulário para Login ou Cadastro

### Requirement: Encerramento de Sessão (Logout)
O sistema SHALL disponibilizar a opção de Logout quando o usuário estiver autenticado, permitindo encerrar a sessão local de forma segura.

#### Scenario: Usuário aciona o botão de logout
- **WHEN** o usuário autenticado clica no botão de Logout
- **THEN** o sistema SHALL remover o token e dados de sessão de `st.session_state` e retornar a visualização para a tela de autenticação

### Requirement: Configuração de URL Base via Arquivo .env
O sistema SHALL carregar a URL base dos endpoints de autenticação a partir da variável de ambiente `XANO_AUTH_BASE_URL` configurada no arquivo `.env` na raiz do projeto.

#### Scenario: Leitura bem-sucedida da variável de ambiente
- **WHEN** a aplicação inicializa ou executa as requisições de autenticação
- **THEN** o sistema SHALL ler `XANO_AUTH_BASE_URL` do `.env` (com fallback seguro ou alerta amigável se não estiver definida) e utilizar essa URL como base para as rotas `auth/login`, `auth/signup` e `auth/me`
