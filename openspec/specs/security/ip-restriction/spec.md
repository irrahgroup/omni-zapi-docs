# security/ip-restriction Specification

## Purpose
Define o que a documentação promete sobre a lista de IPs permitidos do workspace e sobre a recusa de chamadas por IP, para que o cliente configure a restrição sem bloquear a si mesmo.

## Requirements

### Requirement: Regras de funcionamento da lista de IPs

A página Restrição de IP SHALL afirmar que lista vazia permite chamadas de qualquer IP e que, com IPs cadastrados, só eles podem chamar rotas autenticadas por **Secret Key**. A página SHALL afirmar que a comparação é exata, sem faixas nem CIDR, e que `X-Forwarded-For` e cabeçalhos semelhantes são ignorados.

Fonte (`pennsylvania-frisco@develop`): `src/main/java/com/irrahtech/pennsylvaniafrisco/core/domain/IpWhiteList.java:35` — `IpWhiteList.isIpAllowed`; `src/main/java/com/irrahtech/pennsylvaniafrisco/core/domain/WhitelistIps.java:12` — `WhitelistIps.matches`; `src/main/java/com/irrahtech/pennsylvaniafrisco/core/usecase/service/ValidateAuthorizationService.java:30` — `ValidateAuthorizationService.resolveBySecretKey`; `src/main/java/com/irrahtech/pennsylvaniafrisco/entrypoint/http/shared/ClientIp.java:10` — `ClientIp`.

#### Scenario: Lista vazia

- **WHEN** o leitor consulta as regras
- **THEN** a página diz que sem IP cadastrado qualquer IP pode chamar a API

#### Scenario: Lista preenchida

- **WHEN** o leitor consulta as regras
- **THEN** a página diz que só os IPs cadastrados chamam rotas com Secret Key
- **AND** diz que o IP é comparado exatamente como cadastrado e que não há CIDR
- **AND** diz que `X-Forwarded-For` é ignorado

#### Scenario: Rota com Public Key

- **WHEN** o leitor consulta o alcance da regra
- **THEN** a página diz que a regra vale para chamadas com Secret Key, e não para chamadas com Public Key

### Requirement: Prazo de propagação

A página SHALL informar que uma alteração na lista pode levar até 10 minutos para valer na API.

Fonte (`pennsylvania-frisco@develop`): `src/main/java/com/irrahtech/pennsylvaniafrisco/dataprovider/repository/IpWhiteListProvider.java:16` — `IpWhiteListProvider.CACHE_TTL`.

#### Scenario: Aviso de prazo

- **WHEN** o leitor termina o passo a passo de cadastro
- **THEN** a página avisa que a mudança pode levar até 10 minutos

### Requirement: Resposta de bloqueio

A página SHALL documentar que a chamada bloqueada responde `400` com `{"error": "<ip> not allowed"}`, e com `{"error": "ip not allowed"}` quando a API não identifica o IP de origem.

Fonte (`pennsylvania-frisco@develop`): `src/main/java/com/irrahtech/pennsylvaniafrisco/core/usecase/service/ValidateIpWhitelistService.java:20` — `ValidateIpWhitelistService.validate`; `src/main/java/com/irrahtech/pennsylvaniafrisco/config/GlobalExceptionHandler.java:38` — `GlobalExceptionHandler.handleValidation`.

#### Scenario: IP fora da lista

- **WHEN** o leitor consulta a resposta de bloqueio
- **THEN** vê o status `400` e o corpo `{"error": "203.0.113.7 not allowed"}` com o IP bloqueado no lugar de `<ip>`

#### Scenario: IP não identificado

- **WHEN** o leitor consulta a resposta de bloqueio
- **THEN** vê também o corpo `{"error": "ip not allowed"}` e a explicação de quando ele ocorre

### Requirement: Passo a passo de cadastro e quem pode alterar

A página SHALL explicar como cadastrar IPs no painel (descrição opcional por IP), que a gravação pede confirmação por código enviado ao usuário e que só o Owner altera a lista.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/core/usecase/interactor/system/IpWhiteListInteractor.java:39` — `IpWhiteListInteractor.saveOrUpdate`; `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/IpWhiteListResource.java:24` — exige `WS_MANAGE_WORKSPACE`.

#### Scenario: Cadastro

- **WHEN** o leitor segue o passo a passo
- **THEN** encontra o caminho no painel, o campo de IP, o campo opcional de descrição, a confirmação por código e o botão de salvar

#### Scenario: Quem pode alterar

- **WHEN** o leitor consulta o passo a passo
- **THEN** a página diz que só o Owner do workspace altera a lista
