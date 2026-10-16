# Proposal

## Why

O Omni Z-API ganhou um servidor MCP somente leitura (`pennsylvania-pittsburgh`, change `mcp-somente-leitura`) e a tela **Administração → Apps conectados** no painel. A documentação não diz como conectar uma IA, o que ela pode ler nem como o workspace controla esse acesso.

## What Changes

- Nova página **Conectar uma IA (MCP)** / **Connect an AI (MCP)** / **Conectar una IA (MCP)**, como sétima página do grupo Segurança nos três idiomas.
- A página abre com os dois caminhos de conexão: apps por OAuth, cadastrados pela plataforma e com envio possível, e IAs pelo MCP, só de leitura. O fluxo de app por OAuth fica para outra página.
- A página traz o endereço do servidor, o fluxo de autorização, o passo a passo curto por cliente (Claude, ChatGPT, Cursor, VS Code e n8n), as ferramentas por permissão, a política do workspace e as regras de segurança.
- A Introdução da seção Segurança ganha a linha e o parágrafo do novo recurso.
- A opção `mcp` de `contextual.options` no `docs.json` é o menu contextual do Mintlify e não muda.

### Fora de escopo

- Página sobre conectar um app por OAuth. Hoje o cliente é cadastrado só pela plataforma (`POST /admin/oauth/clients` no hermitage), sem fluxo de desenvolvedor para documentar.

- Telas dos clientes de IA além do necessário para adicionar o endereço.
- Imagens da tela Apps conectados.

## Capabilities

### New Capabilities

- `security/ai-mcp`: o que a documentação promete sobre a conexão de uma IA pelo MCP.

### Modified Capabilities

- `security/security-section`: o grupo passa de seis para sete páginas, e a Introdução cita o MCP.

## Impact

**Arquivos novos (3):** `{,en/,es/}security/mcp.mdx`.

**Arquivos alterados (4):** `docs.json` e `{,en/,es/}security/introduction.mdx`.

## Questões em aberto

**Publicação.** Em 16/10/2026 `https://mcp.omni.z-api.io/mcp` responde `404` e a tela está desligada em produção. A página só pode ir ao ar quando os dois estiverem em produção.
