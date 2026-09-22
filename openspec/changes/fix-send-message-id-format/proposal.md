# Proposal

## Why

A documentação da API unificada mostra, em todas as respostas `200` dos endpoints de envio, um `messageId` no formato `wamid.HBgNNTU0NDk3MDUwNzg1FQIAERgSM0` — que é o identificador da Meta, não o que o Omni Z-API devolve. A API real retorna um ID interno hexadecimal de 32 caracteres maiúsculos, por exemplo `01A0C92D0C957FE98B73C8BA0CACF741`.

O erro está em 30 arquivos (10 endpoints × 3 idiomas) e induz o cliente a modelar a coluna errada no banco, validar com regex de `wamid.` e falhar ao correlacionar o envio com o evento recebido no webhook.

## What Changes

- Substituir o exemplo `wamid.HBgNNTU0NDk3MDUwNzg1FQIAERgSM0` por `01A0C92D0C957FE98B73C8BA0CACF741` em todas as respostas `200` dos endpoints de envio da API unificada, nos specs OpenAPI de `pt/`, `en/` e `es/`.
- Enriquecer a descrição do campo `messageId` no schema `MessageResponse` dos mesmos 30 arquivos, declarando o formato (hexadecimal, 32 caracteres maiúsculos) nos três idiomas.
- Documentar, nas páginas de introdução de mensagens (PT/EN/ES), que o `messageId` devolvido no envio é o mesmo valor que chega no webhook como `message._id`, permitindo a conciliação entre envio e evento.
- Não é breaking change de API: corrige documentação que já estava divergente do comportamento em produção.

### Fora de escopo

- **Camada de compatibilidade Z-API** (`{pt,en,es}/z-api/openapi.json`, `{,en/,es/}z-api/messages/*.mdx`): mantém deliberadamente o contrato legado `{ "zaapId": "...", "messageId": "D241XXXX732339502B68" }`. Confirmado com o autor da mudança.
- **Payloads de webhook** (`webhooks/payloads.mdx` e specs relacionados): já usam o formato hexadecimal correto em `message._id` e permanecem inalterados.

## Capabilities

### New Capabilities

- `messages/send-response`: contrato documentado da resposta `200` dos endpoints de envio da API unificada — formato do `messageId`, paridade entre os três idiomas e correlação com o `message._id` do webhook.

### Modified Capabilities

<!-- Nenhuma: o projeto ainda não possui specs publicados em openspec/specs/. -->

## Impact

**Specs OpenAPI (30 arquivos)** — exemplo do `200` e descrição do campo `messageId`:

- `pt/messages/`, `en/messages/`, `es/messages/`, cada um com: `openapi.json` (TEXT), `openapi-audio.json`, `openapi-contact.json`, `openapi-image.json`, `openapi-interactive-action.json`, `openapi-interactive-button.json`, `openapi-location.json`, `openapi-sticker.json`, `openapi-template.json`, `openapi-video.json`.

Duas formas de referência convivem e ambas precisam ser tratadas: a maioria dos arquivos centraliza o exemplo em `components.responses.MessageSuccess`, enquanto os `openapi-template.json` declaram o `200` inline dentro da operação.

**Páginas MDX (3 arquivos)** — nota de correlação com o webhook:

- `messages/introduction.mdx` (PT), `en/messages/introduction.mdx`, `es/messages/introduction.mdx`.

**Sem impacto**: código de produção, rotas, `docs.json`, snippets e seção de webhooks.

## Rastreabilidade

ClickUp **HM-430**. A task cobre dois campos e vira duas changes neste repositório; esta trata do `messageId` (RF02). O `id` do canal (RF03) está em `fix-channel-id-examples`. O comentário na task precisa listar os dois PRs.

```
branch   HM-430-corrige-formato-messageid
título   fix(HM-430): corrige formato do messageId nas respostas de envio
```

A nota de correlação entre o `messageId` do envio e o `message._id` do webhook, adicionada nas três páginas de introdução, vai além de RF01-RF04. Foi pedida diretamente pelo autor da mudança e não consta da task — o revisor deve saber que é escopo adicional deliberado.
