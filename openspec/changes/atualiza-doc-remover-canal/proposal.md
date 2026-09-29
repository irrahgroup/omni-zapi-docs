# Proposal

## Why

A página **Remover canal** descreve a exclusão como "permanente" e diz que o canal é "fisicamente removido do sistema". Depois dos PRs da HM-370 (hermitage #111 e frisco #55), o comportamento que o parceiro enxerga mudou em três pontos, e a página ficou desatualizada:

- **Texto de conceituação.** A afirmação de remoção física não vale mais. O que o parceiro precisa saber é o efeito para ele: o canal deixa de poder ser usado e a exclusão não se desfaz pela API. Como é documentação para clientes, o texto não descreve como o sistema guarda o registro.
- **Condição que a página não cita.** O canal precisa estar desconectado, e a API responde `422 INSTANCE_STILL_CONNECTED` quando não está — código que já existe no `openapi-delete.json`, mas não aparece na página.
- **Corpo do erro 502.** O `openapi-delete.json` exemplifica `{"error": 502, "message": "Hermitage deleteChannel failed"}`. O corpo real, confirmado no frisco #55 e na task, é `{"error": "Hermitage deleteChannel failed"}`: `error` é texto, e não há `message`. Um cliente que faz parse do exemplo procura um campo que não vem.

## What Changes

- Reescrever a conceituação de `channels/delete-channel.mdx` (e as versões `en/` e `es/`) sem afirmar remoção física nem descrever o armazenamento interno.
- Acrescentar a condição "canal desconectado" e o link para Desconectar canal.
- Acrescentar a seção **Erro 502**, com o corpo real e a orientação de tentar de novo e acionar o suporte.
- Nos três `openapi-delete.json`: ajustar a descrição do endpoint, trocar o exemplo do `502` e criar o schema `InternalError` (`error` como string).
- Não é breaking change de API: alinha a documentação ao comportamento já em produção.

### Fora de escopo

- **Efeitos da exclusão para o parceiro** (canal excluído libera a vaga do limite on-demand; excluir trial não devolve o trial). Foram avaliados e ficam fora da página por decisão do autor da mudança. As regras seguem definidas por produto na HM-370 e implementadas na hermitage #111.
- **Como o sistema guarda o canal excluído** (exclusão lógica, `excluded = true`, assinatura preservada). É detalhe interno; a documentação é para clientes e não o expõe. A decisão do autor da mudança é que isso não apareça em nenhum ponto da página nem dos OpenAPIs.
- **O período de carência de 40 dias** para excluir canal vindo de trial. Foi removido do código na hermitage #111 por ter sido um erro. A documentação nunca o citou: `grep -rnE "40 d|40 days|40 días|INSTANCE_WITHIN|graceDays" --include="*.mdx" --include="*.json" .` fora de `openspec/` retorna 0 linhas.
- **`INSTANCE_IS_TRIAL`**, citado na descrição da hermitage #111. `gh search code --owner irrahgroup "INSTANCE_IS_TRIAL"` só o encontra em `nebraska-lincoln` (Z-API); não aparece em `pennsylvania-hermitage` nem em `pennsylvania-frisco`. A linha Trial = Sim da tabela de status fica como está, coerente com o QA da HM-405, em que canais em trial foram excluídos com `204`.
- **Consultas e relatórios internos** que ainda não filtram canal excluído: tratados em tarefa separada, sem efeito na documentação.
- **O formato de erro dos demais códigos** (`400`, `401`, `404`, `422`), que segue `{"error": <número>, "message": <texto>}` no `openapi-delete.json`. Não há evidência de divergência; não foi verificado contra a API.

## Capabilities

### New Capabilities

- `channels/channel-deletion`: o que a documentação de Remover canal promete ao parceiro sobre o efeito da exclusão, suas condições e o erro `502`.

### Modified Capabilities

<!-- Nenhuma. -->

## Impact

**Arquivos alterados (6):**

- `{,en/,es/}channels/delete-channel.mdx` — conceituação, condição de desconexão e erro `502`.
- `{pt,en,es}/channels/openapi-delete.json` — descrição do endpoint, exemplo do `502` e schema `InternalError`.

**Sem impacto**: comportamento da API, `docs.json`, demais páginas de canais, seção de webhooks, camada de compatibilidade Z-API.

## Questão em aberto

O corpo `{"error": "Hermitage deleteChannel failed"}` expõe o nome de um serviço interno (`Hermitage`) ao cliente. É a mensagem que a API já devolvia antes desta change e a que o QA validou, então a documentação a reproduz como está. Vale decidir com quem mantém o frisco se a mensagem pública deveria ser genérica; se mudar, a doc muda junto.

## Rastreabilidade

ClickUp **HM-370** — *(QA) API de deletar canal*. Os PRs de código já estão mergeados ou em revisão nos outros repositórios: hermitage #111 e frisco #55. Esta é a change de **documentação** desdobrada da task, no repositório `docs-omni`. O comentário na task precisa listar os PRs dos três repositórios.

```
branch   HM-370-proposta-remover-canal
título   docs(HM-370): propõe atualizar a doc de remover canal
change   atualiza-doc-remover-canal
```
