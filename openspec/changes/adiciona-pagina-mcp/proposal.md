# Proposal

## Why

O Omni Z-API ganhou um servidor MCP (`pennsylvania-pittsburgh`, changes `mcp-somente-leitura` e `mcp-escrita`) e a tela **Administração → Apps conectados** no painel. A documentação não diz como conectar uma IA, o que ela pode fazer nem como o workspace controla esse acesso.

Desde 29–30/10/2026 o MCP está em produção com as 13 ferramentas de consulta e as 7 de alteração ligadas, e o servidor MCP e o servidor de autorização publicam `channels:read`, `templates:read`, `flows:read`, `billing:read`, `templates:write` e `flows:write`.

## What Changes

- Nova página **Conectar uma IA (MCP)** / **Connect an AI (MCP)** / **Conectar una IA (MCP)**, como sétima página do grupo Segurança nos três idiomas.
- **Modelo único (decisão do dono de 16/10/2026):** o conceito é **Apps conectados**. A IA é um app que entra pelo MCP, com o mesmo login e consentimento. A página abre com as duas portas: pelo próprio app (outro tema, sem fluxo de desenvolvedor) e por uma IA, pelo MCP.
- **Regras por contexto** (change `politicas-separadas-apps-e-mcp`): cada porta tem as suas regras, e uma não muda a outra. A página descreve só a aba **MCP** de **Regras de acesso**, com os nomes do painel: **Permitir conexões pelo MCP**, **Exigir aprovação para novas conexões**, **Quais clientes do MCP** (**Só os verificados**, **Verificados e os que se cadastram sozinhos**, **Só os escolhidos**), **Permissões máximas pelo MCP**, **Validade do acesso**, **Exigir verificação em duas etapas** e **Atender o MCP fora da lista de IPs do workspace**.
- **O que a IA pode fazer** é o que as **Permissões máximas pelo MCP** deixam, com as 20 ferramentas desta versão (13 de consulta e 7 de alteração de templates e flows) pela permissão que cada uma exige, o padrão só de consulta e o aviso de que novas operações vão entrar, sem data nem lista.
- **Quem pode alterar templates e flows:** cliente liberado para alterar (o CIMD com host nas listas do selo e de escrita, que em produção é só `claude.ai`, ou o pré-registro verificado com o escopo), Owner com segundo fator, workspace sem lista de IPs e a permissão no teto do MCP.
- **Aprovação** como passo condicional ("se o workspace exigir aprovação"), só para quem não é Owner, porque a opção vem desligada (hermitage #320).
- **Lista de IPs:** o IP da IA nunca é conferido. Com lista, a opção desligada recusa toda chamada da IA pelo MCP, inclusive as servidas pelo hermitage (hermitage #340, change `recurso-do-mcp-respeita-lista-de-ips`); ligada, libera só as consultas. Alteração nunca passa com lista de IPs.
- **Cursor:** se cadastra sozinho. O selo vem pelo retorno web ou pelo app (hermitage #429), e o retorno direto para `localhost` aparece como app no seu computador; para as regras, ele sempre conta como cliente que se cadastra sozinho.
- **Renovação:** a IA renova o acesso sem novo login até a validade das regras (hermitage #428).
- A página traz o endereço do servidor, o botão **Conectar IA** do painel e o passo a passo curto por cliente (Claude, Claude Code, ChatGPT, Cursor, VS Code e n8n).
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

**Clientes que alteram.** A lista de escrita (`OAUTH_MCP_WRITE_CIMD_HOSTS`) é configuração do hermitage. Se outro cliente entrar nela, a linha "Nesta versão, só o Claude" da página muda junto.
