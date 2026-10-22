# Proposal

## Why

O Omni Z-API ganhou um servidor MCP (`pennsylvania-pittsburgh`, change `mcp-somente-leitura`) e a tela **Administração → Apps conectados** no painel. A documentação não diz como conectar uma IA, o que ela pode fazer nem como o workspace controla esse acesso.

## What Changes

- Nova página **Conectar uma IA (MCP)** / **Connect an AI (MCP)** / **Conectar una IA (MCP)**, como sétima página do grupo Segurança nos três idiomas.
- **Modelo único (decisão do dono de 16/10/2026):** o conceito é **Apps conectados**. A IA é um app que entra pelo MCP, com o mesmo login, consentimento e política. A página abre com as duas portas: pelo próprio app (outro tema, sem fluxo de desenvolvedor) e por uma IA, pelo MCP.
- A política vale para todos os apps. As opções próprias de IA (**IAs conectadas**, **Aceitar IAs não verificadas** e **Atender IAs mesmo fora da lista de IPs**) ficam no bloco **Apps que entram pelo MCP (IAs)**, como exceções em cima da política.
- **O que a IA pode fazer** é o que as **Permissões máximas** deixam, com a lista de ferramentas desta versão e o aviso de que novas operações vão entrar, sem data nem lista.
- **Aprovação** como passo condicional ("se o workspace exigir aprovação"), porque a opção é desligada por padrão e depende do hermitage #320.
- **Lista de IPs** sem promessa de bloqueio completo: hoje ela recusa as consultas da IA a canais, templates, flows e webhooks, mas não as servidas pelo hermitage (`account_whoami`, `channel_types_list`, `plans_list`, `billing_summary`) até o hermitage #337. Para cortar todas as IAs, a página manda desligar **IAs conectadas**.
- A página traz o endereço do servidor e o passo a passo curto por cliente (Claude, ChatGPT, Cursor, VS Code e n8n).
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

**Lista de IPs.** Quando o hermitage #337 estiver no ar, a lista passa a recusar toda chamada da IA com a opção desligada, e a página pode dizer isso.

**Aprovação.** O passo condicional só vale quando o hermitage #320 estiver no ar.

**Publicação.** Em 16/10/2026 `https://mcp.omni.z-api.io/mcp` responde `404` e a tela está desligada em produção. A página só pode ir ao ar quando os dois estiverem em produção.
