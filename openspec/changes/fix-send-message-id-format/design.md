# Design

## Context

Ver `proposal.md` — Why para a motivação.

Levantamento do estado atual (confirmado por inspeção dos 30 arquivos):

- **Onde o valor errado vive**: a string literal `wamid.HBgNNTU0NDk3MDUwNzg1FQIAERgSM0` aparece exatamente 30 vezes no repositório, todas em `{pt,en,es}/messages/*.json`. Nenhuma outra seção da documentação — Z-API, webhooks, templates, flows, channels — contém essa string.
- **Duas formas estruturais**: 27 arquivos centralizam o exemplo em `components.responses.MessageSuccess`; os três `openapi-template.json` declaram o `200` inline na operação `POST /v1/channels/{channelId}/messages`. O schema `MessageResponse` existe nos 30 e é idêntico em estrutura, variando só a descrição por idioma (`ID da mensagem enviada` / `Sent message ID` / `ID del mensaje enviado`).
- **Formatação heterogênea**: `en/` usa JSON compacto (objeto de exemplo em uma linha); `pt/` e `es/` usam JSON expandido. Os arquivos são servidos pelo Mintlify a partir do `docs.json`, não passam por build nem por formatter automático.

## Goals / Non-Goals

**Goals:**

- Corrigir o exemplo e a descrição do `messageId` sem introduzir ruído de reformatação no diff.
- Deixar a correção verificável por um comando, não por leitura arquivo a arquivo.
- Cobrir a lacuna que originou o problema: a documentação nunca explicou o formato do identificador nem sua relação com o webhook.

**Non-Goals:**

- Unificar as duas formas estruturais (`MessageSuccess` compartilhado vs. `200` inline). Os `openapi-template.json` divergem por outros motivos além da resposta; refatorá-los amplia o escopo e o risco sem benefício para esta correção.
- Padronizar a formatação JSON entre `en/` e `pt`/`es`.
- Adicionar `pattern` (regex) ao schema `MessageResponse`. Um regex de validação no spec passa a ser um contrato que a API precisa honrar; a descrição em prosa informa o leitor sem criar essa obrigação.

## Decisions

### Substituição textual dirigida, não round-trip de JSON

Reescrever os arquivos com `json.load` + `json.dump` normalizaria indentação e quebras de linha, gerando um diff de milhares de linhas em 30 arquivos e escondendo a mudança real de 30 caracteres. Como `wamid.HBgNNTU0NDk3MDUwNzg1FQIAERgSM0` é uma string literal única no repositório, uma substituição textual escopada a `{pt,en,es}/messages/*.json` atinge exatamente os 30 pontos, funciona igual nas duas formas estruturais e nas duas formatações, e produz um diff de uma linha por arquivo.

*Alternativa considerada*: edição manual arquivo a arquivo — 30 edições equivalentes, com risco alto de omissão silenciosa e sem ganho.

### A descrição do campo é editada por idioma, não em lote

Ao contrário do valor de exemplo, a descrição do `messageId` difere entre os três idiomas. A substituição é feita em três passadas — uma por locale, cada uma casando o texto atual daquele idioma — em vez de uma expressão genérica que tentasse casar os três.

### O escopo de exclusão é garantido pelo caminho, não pela confiança

O comando de substituição é escopado a `{pt,en,es}/messages/*.json`. Isso exclui `{pt,en,es}/z-api/openapi.json` e a seção de webhooks por construção, e não por cuidado do executor. A verificação final confirma que os identificadores dessas seções continuam intactos.

### A nota de correlação vai nas páginas de introdução

A informação de que o `messageId` do envio é o `message._id` do webhook é conceitual e vale para todos os 10 tipos de mensagem. Repeti-la em cada página de envio seria redundante; colocá-la na introdução de mensagens (PT/EN/ES) a entrega uma vez, no ponto em que o leitor está formando o modelo mental da API.

## Risks / Trade-offs

- **Substituição textual atinge ocorrência não prevista** → O escopo por caminho e a contagem esperada (30 antes, 0 depois) tornam qualquer desvio visível imediatamente; o `git diff` deve mostrar exatamente uma linha alterada por arquivo.
- **O valor `01A0C92D0C957FE98B73C8BA0CACF741` é um exemplo real fornecido pelo autor da mudança** → Usado literalmente e de forma idêntica nos 30 pontos e nos três idiomas; um exemplo único evita que o leitor infira significado de variações entre páginas.
- **A afirmação de correlação com o webhook é um compromisso de contrato** → Ela foi confirmada pelo autor da mudança antes de entrar no escopo. Se o comportamento divergir no futuro, a nota precisa ser revista junto com a seção de webhooks.
- **Documentação sem teste automatizado** → A verificação é um `grep` determinístico sobre o repositório, executado ao final e reproduzível por qualquer revisor.

## Migration Plan

Não se aplica: a mudança é somente de documentação, não há estado a migrar. O rollback é a reversão do commit.
