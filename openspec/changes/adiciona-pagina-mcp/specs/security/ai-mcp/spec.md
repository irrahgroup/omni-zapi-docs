# Spec Delta

## Purpose

Define o que a documentação promete sobre a conexão de um assistente de IA ao workspace pelo servidor MCP do Omni Z-API, dentro do modelo único de Apps conectados.

## ADDED Requirements

### Requirement: Apps conectados com duas portas

A página SHALL abrir com o conceito único de **Apps conectados** e dizer que a IA é um app que entra pelo MCP, com o mesmo login e consentimento, e que cada porta tem as suas regras de acesso. A página SHALL apresentar as duas portas: pelo próprio app e por uma IA, pelo MCP. A página MUST dizer que a porta do próprio app é outro tema e MUST NOT descrever o fluxo de desenvolvedor.

Fonte (`pennsylvania-hermitage@main`): `AdminOAuthResource.java` — `POST /admin/oauth/clients`, só para `ADMIN` e `FATHER` da plataforma; `OAuthScope.java` — `MCP_WRITE_SCOPES` com `templates:write` e `flows:write`, e `messages:send` fora do conjunto do MCP; `AppPolicy.java` — uma política por contexto, sem campo lido por uma para decidir a outra.

#### Scenario: Leitor que integra um sistema próprio

- **WHEN** o leitor abre a página
- **THEN** ele vê, antes do passo a passo, as duas portas e que a página trata só da porta do MCP

### Requirement: Endereço e fluxo de conexão

A página SHALL informar o endereço `https://mcp.omni.z-api.io/mcp` e o fluxo: o cliente abre o login, a pessoa escolhe o workspace, vê o que a IA pode fazer e autoriza. A aprovação MUST aparecer só como passo condicional ("se o workspace exigir aprovação"), para quem não é Owner, feita pelo Owner. A página MUST dizer que o acesso aparece na lista de **Apps conectados** e pode ser revogado ali, e que a IA renova o acesso sem novo login até a **Validade do acesso**.

Fonte: `pennsylvania-pittsburgh@main`, `k8s-templates/production/values.yaml` — host `mcp.omni.z-api.io`, rota exata `/mcp`. `pennsylvania-hermitage@main`: `ConsentInteractor.java:277` — aprovação só sem conta de empresa, sem `managesApps` e com `requireOwnerApproval`; `OpaqueRefreshTokenGenerator.java:16-19` — cliente público recebe refresh (#428).

#### Scenario: Endereço

- **WHEN** o leitor copia o endereço da página
- **THEN** o endereço termina em `/mcp`

#### Scenario: Workspace sem aprovação

- **WHEN** o workspace não exige aprovação
- **THEN** o fluxo da página termina na autorização, sem etapa obrigatória de aprovação

### Requirement: O que a IA pode fazer

A página SHALL dizer que a IA pode fazer o que as **Permissões máximas pelo MCP** deixam, que por padrão só as de consultar canais, templates e flows vêm marcadas, e SHALL listar as ferramentas desta versão pela permissão que cada uma exige: **Ver canais e o status deles** (`account_whoami`, `channel_types_list`, `channels_list`, `channels_get`, `webhooks_list`), **Ver templates** (`templates_list`, `templates_get`, `templates_validate`), **Ver flows** (`flows_list`, `flows_get`, `flows_validate`), **Ver cobrança e planos** (`plans_list`, `billing_summary`), **Criar e alterar templates** (`templates_create`, `templates_update`, `templates_sync`, `templates_media_upload`) e **Criar e alterar flows (rascunho)** (`flows_create`, `flows_update`, `flows_sync`). A página MUST dizer que o MCP nunca publica um flow e que novas operações vão entrar. A página MUST NOT afirmar que o MCP é só de leitura nem prometer data ou lista de operações futuras.

Fonte (`pennsylvania-pittsburgh@main`): `app/core/domain/tool.go` — catálogo com o escopo de cada ferramenta; `app/entrypoint/http/tool_definitions.go` — descrições; `k8s-templates/production/values.yaml` — as `MCP_*_READY` ligadas. `pennsylvania-hermitage@main`: `AppPolicy.java:55-58` e `McpPolicy.java:37-40` — teto padrão. Rótulos: `pennsylvania-lancaster@main-omnizapi`, `src/i18n/pt-br.json`, `oauthApps.scopes.*`.

#### Scenario: Cobrança desmarcada

- **WHEN** o leitor consulta o que a IA faz sem **Ver cobrança e planos**
- **THEN** a página diz que ela não consulta cobrança nem planos

#### Scenario: Workspace com as regras padrão

- **WHEN** o leitor não mudou as **Permissões máximas pelo MCP**
- **THEN** a página diz que só as permissões de consultar canais, templates e flows vêm marcadas

### Requirement: Quem pode alterar templates e flows

A página SHALL dizer que marcar a permissão de alterar não basta e listar as condições: cliente liberado para alterar (nesta versão, só o Claude e os apps cadastrados e verificados pela plataforma com a permissão), quem autoriza é o Owner com a autenticação de dois fatores ativa, o workspace sem lista de IPs e a permissão marcada em **Permissões máximas pelo MCP**. A página MUST dizer que ChatGPT, VS Code, Cursor e n8n ficam só com as permissões de consultar.

Fonte (`pennsylvania-hermitage@main`): `McpWriteEligibility.java:53-66`, `McpWriteChecks.java:47-64`, `MembershipRole.java:47-50`, `User.java:284-286`, `k8s/production/values.yaml` — `OAUTH_MCP_WRITE_CIMD_HOSTS: "claude.ai"` e `OAUTH_CIMD_VERIFIED_HOSTS`.

#### Scenario: ChatGPT verificado

- **WHEN** o leitor conecta o ChatGPT com a permissão de alterar marcada
- **THEN** a página diz que ele fica só com as permissões de consultar

#### Scenario: Workspace com lista de IPs

- **WHEN** o workspace tem lista de IPs
- **THEN** a página diz que o MCP não altera nada no workspace, qualquer que seja a opção da lista de IPs

### Requirement: Regras de acesso do MCP

A página SHALL dizer que as regras do MCP ficam em **Regras de acesso**, aba **MCP**, separadas das de **Apps de terceiros**, e SHALL descrever as opções com os nomes do painel: **Permitir conexões pelo MCP**, **Exigir aprovação para novas conexões**, **Quais clientes do MCP** (**Só os verificados**, **Verificados e os que se cadastram sozinhos**, **Só os escolhidos**), **Permissões máximas pelo MCP**, **Validade do acesso**, **Exigir verificação em duas etapas** e **Atender o MCP fora da lista de IPs do workspace**. A página MUST dizer que o Cursor, mesmo com o selo, conta como cliente que se cadastra sozinho e não entra com **Só os verificados**.

Fonte (`pennsylvania-lancaster@main-omnizapi`): `src/pages/app/connected-apps/index.tsx`, `src/components/Common/WorkspaceApps/preview/rules-view.tsx` e `src/i18n/{pt-br,en-us,es}.json` — chaves `connectedAppsPreview.links.rules`, `connectedAppsPreview.rules.*`, `connectedAppsPolicies.mcp.*`, `connectedAppsPolicies.rules.mcpClients.*`. Cursor: `pennsylvania-hermitage@main`, `ClientVerification.java:165-193` (#429).

#### Scenario: Cursor com Só os verificados

- **WHEN** as regras do MCP estão em **Só os verificados**
- **THEN** a página diz que Cursor e n8n não entram

### Requirement: Lista de IPs

A página SHALL dizer que o workspace não confere o IP da IA e que, com lista de IPs, a opção **Atender o MCP fora da lista de IPs do workspace** decide: desligada, o workspace recusa todas as chamadas da IA pelo MCP; ligada, a IA só consulta. A página MUST dizer que alterar exige workspace sem lista de IPs.

Fonte: `pennsylvania-hermitage@main`, `ResourceTokenFilter.java:55-58,154-163` e `EvaluateResourceIpPolicyInteractor.java:34-49` (change `recurso-do-mcp-respeita-lista-de-ips`, #340); `pennsylvania-frisco@main`, `AuthorizeAppRequestInteractor.java:245-259`.

#### Scenario: Workspace com lista de IPs e a opção desligada

- **WHEN** o workspace tem lista de IPs e a opção de atender o MCP está desligada
- **THEN** a página diz que todas as chamadas da IA pelo MCP são recusadas, inclusive as consultas
