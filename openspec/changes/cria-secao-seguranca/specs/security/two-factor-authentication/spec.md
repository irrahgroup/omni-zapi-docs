# Spec Delta

## Purpose

Define o que a documentação promete sobre a autenticação de dois fatores (2FA) do login no painel do Omni Z-API e deixa claro o que ela não cobre.

## ADDED Requirements

### Requirement: Escopo do 2FA

A página SHALL afirmar que o 2FA protege o **login no painel** e que ele **não altera** a autenticação da API, que segue por Public Key e Secret Key.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/identity/UserResource.java:377` — parâmetro `code2fa` do login de usuário; `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/security/JwtTokenService.java:257` — `JwtTokenService.authenticateBySecretKey`, caminho da Secret Key sem 2FA.

#### Scenario: Escopo

- **WHEN** o leitor consulta o escopo
- **THEN** a página diz que o 2FA vale para o login no painel
- **AND** diz que chamadas de API com chave continuam iguais

### Requirement: Ativação e desativação

A página SHALL explicar como ativar o 2FA com um app autenticador (leitura do QR code ou código manual e confirmação com código de 6 dígitos) e como desativá-lo.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/identity/UserResource.java:595` — `create-2fa`; `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/identity/UserResource.java:601` — `active-2fa/{code}`. Fonte do fluxo na tela (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` chaves `hubMessageActive2FA.*`.

#### Scenario: Ativar

- **WHEN** o leitor segue o passo a passo
- **THEN** encontra o caminho no painel, o QR code, o código manual e o código de 6 dígitos que conclui a ativação

#### Scenario: Entrar com 2FA ativo

- **WHEN** o leitor consulta o login com 2FA ativo
- **THEN** a página diz que, além da senha, o painel pede o código do app autenticador

#### Scenario: Desativar

- **WHEN** o leitor consulta a desativação
- **THEN** a página explica como desativar e avisa que a conta fica menos protegida
