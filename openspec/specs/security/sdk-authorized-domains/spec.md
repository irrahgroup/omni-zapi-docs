# security/sdk-authorized-domains Specification

## Purpose
Define o que a documentação promete sobre os domínios onde a SDK de conexão de canais pode abrir, para que o cliente cadastre as origens do seu site corretamente.

## Requirements

### Requirement: Cadastro de domínios por origem exata

A página Domínios da SDK SHALL explicar como cadastrar domínios no painel e que cada domínio é comparado como **origem exata** (esquema, host e porta, por exemplo `https://app.example.com`). A página MUST NOT afirmar que a SDK aceita curinga. A página SHALL avisar que um site em origem não cadastrada não consegue abrir a SDK.

Fonte (`pennsylvania-lester@omnizapi`): `src/core/client.ts:416` — comparação `currentOrigin === new URL(origin).origin`; `src/core/client.ts:70` — código de falha `origin_not_allowed`.

#### Scenario: Origem cadastrada

- **WHEN** o leitor consulta as regras
- **THEN** a página diz que a origem do site precisa constar na lista, escrita por inteiro, com esquema e porta quando houver

#### Scenario: Sem curinga

- **WHEN** o leitor procura suporte a curinga
- **THEN** a página diz que cada subdomínio precisa ser cadastrado à parte
- **AND** o texto não contém `*.` como exemplo válido de cadastro

#### Scenario: Origem não cadastrada

- **WHEN** o leitor consulta o que acontece com uma origem fora da lista
- **THEN** a página diz que a SDK não abre e devolve a falha `origin_not_allowed`

### Requirement: Painel do Omni sempre liberado

A página SHALL informar que as origens do painel do Omni Z-API são sempre aceitas, mesmo com a lista vazia, e não precisam ser cadastradas.

Fonte (`pennsylvania-frisco@develop`): `src/main/java/com/irrahtech/pennsylvaniafrisco/core/usecase/interactor/GetSdkInfoInteractor.java:71` — `GetSdkInfoInteractor.withPanelOrigins`; `src/main/resources/application.yaml:33` — `sdk.panel-origins`.

#### Scenario: Lista vazia

- **WHEN** o leitor consulta a lista vazia
- **THEN** a página diz que o painel do Omni continua funcionando e que o site do cliente só funciona depois de cadastrado

### Requirement: Quem configura

A página SHALL dizer que só o Owner do workspace altera os domínios.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/clientapp/SdkConfigResource.java:47` — exige `WS_MANAGE_WORKSPACE`.

#### Scenario: Papel necessário

- **WHEN** o leitor consulta quem configura
- **THEN** a página diz que a configuração é restrita ao Owner
