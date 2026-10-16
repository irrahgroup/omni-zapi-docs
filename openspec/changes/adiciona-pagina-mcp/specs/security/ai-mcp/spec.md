# Spec Delta

## Purpose

Define o que a documentação promete sobre a conexão de um assistente de IA ao workspace pelo servidor MCP do Omni Z-API, dentro do modelo único de Apps conectados.

## ADDED Requirements

### Requirement: Apps conectados com duas portas

A página SHALL abrir com o conceito único de **Apps conectados** e dizer que a IA é um app que entra pelo MCP, com o mesmo login, consentimento e política. A página SHALL apresentar as duas portas: pelo próprio app e por uma IA, pelo MCP. A página MUST dizer que a porta do próprio app é outro tema e MUST NOT descrever o fluxo de desenvolvedor.

Fonte (`pennsylvania-hermitage@develop`): `AdminOAuthResource.java` — `POST /admin/oauth/clients`, só para `ADMIN` e `FATHER` da plataforma; `OAuthScope.java` — `messages:send`, `templates:write` e `flows:write` fora do conjunto do MCP.

#### Scenario: Leitor que integra um sistema próprio

- **WHEN** o leitor abre a página
- **THEN** ele vê, antes do passo a passo, as duas portas e que a página trata só da porta do MCP

### Requirement: Endereço e fluxo de conexão

A página SHALL informar o endereço `https://mcp.omni.z-api.io/mcp` e o fluxo: o cliente abre o login, a pessoa escolhe o workspace, vê o que a IA pode fazer e autoriza. A aprovação MUST aparecer só como passo condicional ("se o workspace exigir aprovação"), feita pelo Owner. A página MUST dizer que o acesso aparece em **Apps conectados ao workspace** e pode ser revogado ali.

Fonte (`pennsylvania-pittsburgh@develop`): `k8s-templates/production/values.yaml` — host `mcp.omni.z-api.io`, rota exata `/mcp`. Aprovação: `pennsylvania-hermitage` #320, ainda aberto.

#### Scenario: Endereço

- **WHEN** o leitor copia o endereço da página
- **THEN** o endereço termina em `/mcp`

#### Scenario: Workspace sem aprovação

- **WHEN** o workspace não exige aprovação
- **THEN** o fluxo da página termina na autorização, sem etapa obrigatória de aprovação

### Requirement: O que a IA pode fazer

A página SHALL dizer que a IA pode fazer o que as **Permissões máximas** da política deixam e SHALL listar as ferramentas desta versão pela permissão que cada uma exige: **Ver canais** (`account_whoami`, `channel_types_list`, `channels_list`, `channels_get`, `webhooks_list`), **Ver templates** (`templates_list`, `templates_get`, `templates_validate`), **Ver flows** (`flows_list`, `flows_get`, `flows_validate`) e **Ver cobrança e planos** (`plans_list`, `billing_summary`). A página MUST dizer que novas operações vão entrar. A página MUST NOT afirmar que o MCP é só de leitura nem prometer data ou lista de operações futuras.

Fonte (`pennsylvania-pittsburgh@develop`): `app/core/domain/tool.go` — catálogo com o escopo de cada ferramenta.

#### Scenario: Cobrança desmarcada

- **WHEN** o leitor consulta o que a IA faz sem **Ver cobrança e planos**
- **THEN** a página diz que ela não consulta cobrança nem planos

### Requirement: Política para todos os apps e exceções das IAs

A página SHALL dizer que a política vale para todos os apps conectados. As opções **IAs conectadas**, **Aceitar IAs não verificadas** e **Atender IAs mesmo fora da lista de IPs** MUST ficar num bloco **Apps que entram pelo MCP (IAs)**, como exceções em cima da política. A página MUST NOT prometer que a lista de IPs bloqueia todo acesso da IA: com a opção desligada, ela diz só que o workspace recusa as consultas a canais, templates, flows e webhooks, e manda desligar **IAs conectadas** para cortar todas as IAs.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` — chaves `connectedApps.ai.*`, `connectedApps.policy.*`, `selfRegisteredApps.unverified.*`. Lista de IPs: `pennsylvania-hermitage` #337 — o `ResourceTokenFilter` não aplica a lista às rotas `/resource/v1/**`, e o frisco aplica.

#### Scenario: Workspace com lista de IPs

- **WHEN** o workspace tem lista de IPs e a opção de atender IAs está desligada
- **THEN** a página diz que as consultas da IA a canais, templates, flows e webhooks são recusadas
- **AND** a página não diz que todo acesso da IA é recusado
