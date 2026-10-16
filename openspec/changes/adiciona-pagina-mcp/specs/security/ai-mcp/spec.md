# Spec Delta

## Purpose

Define o que a documentação promete sobre a conexão de um assistente de IA ao workspace pelo servidor MCP do Omni Z-API.

## ADDED Requirements

### Requirement: Dois caminhos de conexão

A página SHALL abrir dizendo que os apps conectados chegam por dois caminhos: apps por OAuth, cadastrados pela plataforma, que usam a API com as permissões autorizadas, envio de mensagens incluído; e IAs pelo MCP, um caso dentro dos apps conectados, só de leitura. A página MUST dizer que conectar um app por OAuth é outro tema e MUST NOT descrever o fluxo de desenvolvedor.

Fonte (`pennsylvania-hermitage@develop`): `AdminOAuthResource.java` — `POST /admin/oauth/clients`, só para `ADMIN` e `FATHER` da plataforma; `OAuthScope.java` — `messages:send`, `templates:write` e `flows:write` fora do conjunto do MCP.

#### Scenario: Leitor que integra um sistema próprio

- **WHEN** o leitor abre a página
- **THEN** ele vê, antes do passo a passo, que apps por OAuth são outro caminho, com envio possível, e que a página trata só das IAs

### Requirement: Endereço e fluxo de conexão

A página SHALL informar o endereço `https://mcp.omni.z-api.io/mcp` e o fluxo: o cliente abre o login, a pessoa escolhe o workspace, vê o que a IA pode fazer e autoriza. A página MUST dizer que o acesso aparece em **Apps conectados ao workspace** e pode ser revogado ali.

Fonte (`pennsylvania-pittsburgh@develop`): `k8s-templates/production/values.yaml` — host `mcp.omni.z-api.io`, rota exata `/mcp`; `openspec/changes/mcp-somente-leitura/specs/servidor-mcp/spec.md` — `POST /mcp`.

#### Scenario: Endereço

- **WHEN** o leitor copia o endereço da página
- **THEN** o endereço termina em `/mcp`

### Requirement: Somente leitura e ferramentas por permissão

A página SHALL dizer que a IA só lê e SHALL listar as 13 ferramentas pela permissão que cada uma exige: **Ver canais** (`account_whoami`, `channel_types_list`, `channels_list`, `channels_get`, `webhooks_list`), **Ver templates** (`templates_list`, `templates_get`, `templates_validate`), **Ver flows** (`flows_list`, `flows_get`, `flows_validate`) e **Ver cobrança e planos** (`plans_list`, `billing_summary`). A página MUST dizer que a IA não recebe mais do que **Permissões máximas**.

Fonte (`pennsylvania-pittsburgh@develop`): `app/core/domain/tool.go` — catálogo com o escopo de cada ferramenta.

#### Scenario: Cobrança desmarcada

- **WHEN** o leitor consulta o que a IA lê sem **Ver cobrança e planos**
- **THEN** a página diz que ela não lê cobrança nem planos

### Requirement: Política e segurança

A página SHALL descrever as opções de **Ver a política** e SHALL dizer que: IAs não verificadas só entram com **Aceitar IAs não verificadas** ou liberadas em **Apps permitidos**; a lista de IPs recusa as IAs, a não ser que **Atender IAs mesmo fora da lista de IPs** esteja ligado; desligar **IAs conectadas** corta todas as IAs sem revogar os outros apps.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` — chaves `connectedApps.ai.*`, `connectedApps.policy.*`, `selfRegisteredApps.unverified.*`.

#### Scenario: Workspace com lista de IPs

- **WHEN** o workspace tem lista de IPs e a opção de atender IAs está desligada
- **THEN** a página diz que a leitura pela IA é recusada
