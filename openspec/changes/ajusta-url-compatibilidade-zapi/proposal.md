# Proposal

## Why

A camada de compatibilidade Z-API ganha host próprio: passa de `api.omni.z-api.io` para `zapi.omni.z-api.io`. A documentação ainda aponta para o host antigo em 15 pontos, e quem copiar um exemplo hoje chama o endereço errado.

A separação faz sentido: a compatibilidade Z-API e a API unificada são superfícies distintas, com contratos distintos, e até agora dividiam o mesmo hostname.

## What Changes

- Trocar `https://api.omni.z-api.io` por `https://zapi.omni.z-api.io` nas 15 ocorrências dentro de `*/z-api/` — 9 arquivos, nos três idiomas.
- Alcança o `servers[0].url` dos três `openapi.json`, os exemplos `curl` das páginas de autenticação e introdução, e o lado direito das tabelas de comparação.

### Fora de escopo

- **A API unificada** (`messages`, `channels`, `webhooks`, `templates`): continua em `api.omni.z-api.io`, com 79 ocorrências em 75 arquivos. Confirmado com o autor da mudança — só a camada de compatibilidade muda de host.
- **`api.z-api.io`**, a Z-API original: aparece no lado esquerdo das tabelas de comparação e nos textos de migração, representando de onde o cliente vem. Não muda, e é string distinta, então a substituição não a alcança.
- **`snippets/variables.mdx`**: as variáveis `zapiBaseUrl` e `zapiOriginalUrl` estão comentadas e sem uso. Mantê-las fora daqui preserva o PR #12, que propõe remover os imports quebrados. Ver Questão em aberto.

## Capabilities

### New Capabilities

- `z-api/base-url`: host documentado da camada de compatibilidade Z-API, e a fronteira entre ele, o host da API unificada e o da Z-API original.

### Modified Capabilities

<!-- Nenhuma. -->

## Impact

**9 arquivos, 15 ocorrências:**

| Arquivo | Ocorrências |
|---|---|
| `{,en/,es/}z-api/introduction.mdx` | 3 cada — tabela de comparação, `curl`, texto de migração |
| `{,en/,es/}z-api/authentication.mdx` | 1 cada — `curl` |
| `{pt,en,es}/z-api/openapi.json` | 1 cada — `servers[0].url` |

**Sem impacto**: specs da API unificada, `docs.json`, snippets, seção de webhooks.

## Questão em aberto

Uma troca de host é exatamente o caso de uso de uma variável de snippet. Com `zapiBaseUrl` ativa e usada, a próxima mudança seria uma linha em vez de 15. Hoje ela está comentada e os imports quebrados são alvo do PR #12, que propõe removê-los.

Vale decidir depois se a compatibilidade passa a usar variável — o que muda o rumo daquele PR. Esta change mantém o valor literal para não atropelá-lo.

## Rastreabilidade

ClickUp **HM-409** — *Rota de compatibilidade Z-API recusa envio por qualquer canal que não seja META_WHATSAPP*.

A HM-409 é um hotfix de backend no `pennsylvania-reading`, já concluído, e os critérios de aceite CA01–CA08 tratam do gate de `META_WHATSAPP`, não da documentação. O que amarra esta change à task é a afirmação no enunciado dela:

> servida hoje pelo `pennsylvania-reading` em `zapi.hubmessage.io` (host que passará a ser `zapi.omni.z-api.io`)

É a habilitação desse host que esta change documenta. **Nenhum critério de aceite da HM-409 é cumprido aqui** — isto é o desdobramento em documentação de uma decisão registrada nela.

Duas observações que a leitura da task levantou:

- O host vigente segundo a task é `zapi.hubmessage.io`, e a palavra `hubmessage` **não aparece em nenhum lugar da documentação**. Ou seja, a doc nunca documentou o host real desta rota: apontava para `api.omni.z-api.io`. Esta change a alinha ao host de destino, não ao vigente.
- O `curl` de evidência da task usa `/instances/`, e o spec usa `/channels/`. Não é divergência: `z-api/introduction.mdx:34` documenta que a rota aceita os dois.

```
branch   ajusta-url-compatibilidade-zapi
título   fix(HM-409): aponta a compatibilidade Z-API para zapi.omni.z-api.io
```
