# Proposal

## Why

A documentação apresenta o ID de canal em dois formatos incompatíveis. Em 48 lugares ele aparece como hexadecimal de 32 caracteres maiúsculos (`019E4C54B1B375A28970B605CA9B03C3`), que é o formato real. Em 6 lugares aparece como UUID (`a1b2c3d4-e5f6-7890-abcd-ef1234567890`), que a API não devolve.

Os 6 pontos errados estão no caminho de entrada do integrador — as duas primeiras chamadas que ele faz:

- **Criar canal**: o exemplo de resposta `200`, verificado renderizado em `/channels/create-channel`.
- **Conectar canal**: o exemplo do parâmetro `channelId`, cuja própria descrição diz "ID do canal (obtido via Criar canal)".

O efeito é pior que um exemplo feio: quem cria o canal recebe um UUID de mentira, leva esse formato para o parâmetro de conexão, e só descobre o formato verdadeiro ao ver a resposta real ou algum dos outros 48 exemplos. Corrigir os dois juntos preserva a narrativa criar → conectar com o mesmo ID.

## What Changes

- Substituir `a1b2c3d4-e5f6-7890-abcd-ef1234567890` por `019E4C54B1B375A28970B605CA9B03C3` em 6 pontos: o exemplo de resposta de `openapi-create.json` e o exemplo do parâmetro `channelId` de `openapi-connect.json`, nos três idiomas.
- Reusar o valor que já aparece nos outros 48 lugares, em vez de introduzir um valor novo, para que o leitor siga criar → conectar → enviar com o mesmo identificador.
- Não é breaking change de API: corrige documentação já divergente do comportamento em produção.

### Fora de escopo

- **O spec órfão `openapi-create-channel.json`**: existe em `pt/` e `es/` (não em `en/`), está registrado no array `openapi` do `docs.json`, mas nenhuma página `.mdx` o referencia — logo não é exibido. Ele descreve o mesmo path `POST /v1/channels` com resposta `201`, erros `400`/`422` e requisito de role ENTERPRISE, e já usa o formato hexadecimal correto. Fica intocado por decisão do autor da mudança. Ver Questão em aberto.
- **Os UUIDs em `openapi-sticker.json`**: `05bc83ea-...` e `f8c95807-...` compõem uma URL de pacote de figurinhas em CDN externo. São UUIDs legítimos de outro sistema, não identificadores de canal.

## Capabilities

### New Capabilities

- `channels/channel-identifier`: formato do identificador de canal na documentação — o que a criação devolve, e a consistência desse valor ao longo das chamadas que o consomem.

### Modified Capabilities

<!-- Nenhuma. -->

## Impact

**Arquivos alterados (6)**, uma linha cada:

- `{pt,en,es}/channels/openapi-create.json:49` — exemplo da resposta.
- `pt/channels/openapi-connect.json:22`, `en/channels/openapi-connect.json:22`, `es/channels/openapi-connect.json:34` — exemplo do parâmetro `channelId`. A linha difere em `es/` porque o arquivo usa formatação expandida.

**Sem impacto**: comportamento da API, `docs.json`, páginas `.mdx`, specs de mensagens, seção de webhooks, spec órfão.

## Questão em aberto

Os dois specs de `POST /v1/channels` divergem em código de status (`200` × `201`), `operationId` (`createChannel` × `partnerCreateChannel`) e pré-requisito de permissão. Não dá para decidir pelo repositório se são duas rotas distintas que colidiram no mesmo path, ou se o órfão é uma reescrita que nunca foi ligada à página. Precisa de confirmação com quem conhece a rota, e de change própria depois disso.

## Rastreabilidade

ClickUp **HM-430**, que na revisão de 2026-09-22 passou a cobrir os dois campos: `messageId` (RF02) e `id` (RF03). A task é a unidade do problema e vira duas changes neste repositório:

| Change | Campo | Estado |
|---|---|---|
| `fix-send-message-id-format` | `messageId` nas rotas de envio | implementada |
| `fix-channel-id-examples` | `id` do canal | esta |

O comentário na task precisa listar os **dois** PRs.

```
branch   HM-430-corrige-formato-id-do-canal
título   fix(HM-430): corrige formato do id do canal nos exemplos
```

Uma nota sobre o parâmetro `channelId` do `openapi-connect.json`: a RF03 fala em exemplos do campo `id` em retornos, e esse é um parâmetro de caminho, não um retorno. Entra pela RF04 e pela CA03, que pedem consistência entre as rotas impactadas, e por decisão explícita do autor da mudança. Vale o revisor confirmar.
