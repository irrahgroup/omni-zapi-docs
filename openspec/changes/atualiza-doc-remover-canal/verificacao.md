# Verificacao de atualiza-doc-remover-canal

Gerado por `verificar.mjs` em 2026-09-29 e preenchido pelo verificador. As medicoes vieram de execucao.
Base da comparacao: `origin/HM-370-proposta-remover-canal`. Commit verificado: `00e2dd3`.

## Cobertura dos cenarios

Cada cenario abaixo cita `arquivo:linha` e o trecho exato. PT = `channels/`, EN = `en/channels/`, ES = `es/channels/`.

### Requirement: A exclusão é descrita pelo efeito para o parceiro

Cenario **Conceituacao da pagina** (coberto, 3 idiomas):

- PT `channels/delete-channel.mdx:11` -- "Exclui um canal. Depois de excluído, o canal deixa de poder ser usado, e não é possível desfazer a exclusão pela API."
- EN `en/channels/delete-channel.mdx:11` -- "Deletes a channel. Once deleted, the channel can no longer be used, and deletion cannot be undone through the API."
- ES `es/channels/delete-channel.mdx:11` -- "Elimina un canal. Una vez eliminado, el canal ya no se puede usar, y el borrado no se puede deshacer mediante la API."
- Ausencia dos termos: `grep -rniE 'fisicamente|physically|físicamente|permanentemente|permanently'` nos 3 `.mdx` e nos 3 JSON retorna vazio (saida 1).

Cenario **Descricao do endpoint** (coberto, 3 idiomas):

- PT `pt/channels/openapi-delete.json:13` -- "Exclui um canal. A exclusão só é permitida quando o canal não possui assinatura ativa (status `CANCELED`, `TRIAL` ou `PENDING`). Requer role ENTERPRISE."
- EN `en/channels/openapi-delete.json:13` -- "Deletes a channel. Deletion is only allowed when the channel has no active subscription (...). Requires ENTERPRISE role."
- ES `es/channels/openapi-delete.json:21` -- "Elimina un canal. Solo se permite el borrado cuando el canal no tiene una suscripción activa (...). Requiere el rol ENTERPRISE."
- O texto antigo ("Remove permanentemente um canal e todos os seus dados") saiu: `git diff` de `pt/channels/openapi-delete.json` linha 13.

Clausula MUST NOT (termos internos): `grep -rniE 'lógic|logical|lógico|soft|excluded|preserv|registro|record'` nos 6 arquivos retorna vazio (saida 1).

### Requirement: Condição de canal desconectado

Cenario **Canal ainda conectado** (coberto, 3 idiomas):

- PT `channels/delete-channel.mdx:19` -- "só é permitida quando o canal está [desconectado](/channels/disconnect) ... a API responde `422` com `INSTANCE_STILL_CONNECTED`."
- EN `en/channels/delete-channel.mdx:19` -- "only allowed when the channel is [disconnected](/en/channels/disconnect) ... returns `422` with `INSTANCE_STILL_CONNECTED`."
- ES `es/channels/delete-channel.mdx:19` -- "cuando está [desconectado](/es/channels/disconnect) ... responde `422` con `INSTANCE_STILL_CONNECTED`."
- Os alvos existem: `channels/disconnect.mdx`, `en/channels/disconnect.mdx`, `es/channels/disconnect.mdx` estao no disco e em `docs.json:180`, `docs.json:448`, `docs.json:716`.
- OpenAPI ja trazia o exemplo: `pt/channels/openapi-delete.json:80`, `en/channels/openapi-delete.json:80`, `es/channels/openapi-delete.json:114` -- `"message": "INSTANCE_STILL_CONNECTED"`.

Cenario **Paridade entre idiomas** (coberto para a condicao; lacuna na parte "mesmo corpo de erro"):

- As tres paginas trazem a mesma condicao e o mesmo codigo (linhas 19 acima) e o mesmo corpo do 502 (linha 38 das tres: `{ "error": "Hermitage deleteChannel failed" }`).
- **Lacuna de precisao da spec**: "o mesmo corpo de erro" nao diz de qual erro. A pagina cita o `422` so pelo codigo, sem corpo JSON; o corpo do `422` aparece so no OpenAPI (`{ "error": 422, "message": "INSTANCE_STILL_CONNECTED" }`, identico nos tres). Li como "corpo do 502 igual nos tres", que esta provado. A spec deveria dizer qual corpo.

### Requirement: Corpo do erro 502

Cenario **Exemplo do 502 no OpenAPI** (coberto, 3 idiomas):

- PT `pt/channels/openapi-delete.json:94-95` -- `"schema": { "$ref": "#/components/schemas/InternalError" }`, `"example": { "error": "Hermitage deleteChannel failed" }`
- EN `en/channels/openapi-delete.json:94-95` -- mesmo trecho.
- ES `es/channels/openapi-delete.json:132-137` -- `"$ref": "#/components/schemas/InternalError"`, `"example": { "error": "Hermitage deleteChannel failed" }` (formatado em varias linhas).
- Schema `InternalError` com `error` string e sem `message`: PT `pt/channels/openapi-delete.json:126-131`, EN `en/channels/openapi-delete.json:126-131`, ES `es/channels/openapi-delete.json:173-180` -- `"properties": { "error": { "type": "string" } }`.
- Checagem propria em Python nos 3 JSON: exemplo igual a `{"error":"Hermitage deleteChannel failed"}`, sem `message`, `$ref` para `InternalError`, `error` do tipo `string`. Resultado: nenhum idioma violou.
- `Error` (`error` integer + `message`) segue nos demais codigos, como o proposal declara (fora de escopo).

Cenario **Secao de erro na pagina** (coberto, 3 idiomas):

- PT `channels/delete-channel.mdx:33-39` -- "### Erro `502`" / "Tente novamente e, se o erro persistir, fale com o suporte." / `{ "error": "Hermitage deleteChannel failed" }`
- EN `en/channels/delete-channel.mdx:33-39` -- "Try again and, if the error persists, contact support." / mesmo JSON.
- ES `es/channels/delete-channel.mdx:33-39` -- "Inténtalo de nuevo y, si el error persiste, contacta con soporte." / mesmo JSON.
- Sem timestamp, path nem status interno: o bloco de codigo tem so o campo `error` (linha 38 nas tres); os textos dizem "sem detalhes internos".

## O gate deste repositorio

Este repositorio nao tem suite de testes nem `.github/workflows/`. O gate e manual, executado pelo verificador.

- comando: `python3 scripts/check-docs.py && openspec validate atualiza-doc-remover-canal`
- resultado: **passou** (saida 0). `check-docs: tudo certo`; `Change 'atualiza-doc-remover-canal' is valid`.
- validacao JSON dos 3 `*/channels/openapi-delete.json`: `ok`.
- testes executados: 0 (nao ha testes de codigo; `--sensor` do script nao se aplica).
- Observacao do script: `verificar.mjs` recusa rodar com mais de uma change ativa e nao le specs em `specs/<area>/<capacidade>/spec.md` (2 niveis), por isso gerou zero requisitos e "0 arquivos" de impacto. Rodei numa worktree temporaria so com esta change; a cobertura acima e a lista de impacto abaixo sao manuais.

## Garantias tocadas

O cruzamento automatico (`impacto-da-change.mjs`) nao mediu nada: nao ha `openspec/specs/` consolidado para esta capacidade. Conferencia manual:

- `git diff origin/HM-370-proposta-remover-canal --stat` lista 7 arquivos: 3 `delete-channel.mdx`, 3 `openapi-delete.json` e `openspec/changes/atualiza-doc-remover-canal/tasks.md`. Nenhum fora da lista esperada.
- `docs.json` nao aparece no diff.
- Novos links internos (`/channels/disconnect`, `/en/channels/disconnect`, `/es/channels/disconnect`) apontam para paginas existentes e registradas em `docs.json`.
- Linha de base da proposta (tarefa 1.1): `grep` por `40 d|40 days|40 días|INSTANCE_WITHIN|graceDays` em `*.mdx`/`*.json` fora de `openspec/` retorna vazio.

## Sensor de discriminacao

Adaptado para documentacao: em vez de rodar testes, roda-se a checagem da tarefa 4.1 e uma checagem propria do 502. O `grep -rniE` da 4.1 foi reproduzido em Python (mesma regex, sem distinguir maiuscula) para poder rodar dentro da worktree temporaria.

Procedimento: linha de base `git status --porcelain` vazia; `git worktree add --detach /tmp/vmut HEAD`; mutacoes na copia; worktree removida; `git status --porcelain` vazio de novo.

- Base (sem mutacao): 4.1 = 0 ocorrencias; termos da 1.2 = 0; 502 = nenhum idioma violado.
- M1 PT, `channels/delete-channel.mdx:11` trocado por "é removido fisicamente do sistema (exclusão lógica)": a 4.1 detectou (`channels/delete-channel.mdx:11`) e a busca da 1.2 tambem. **Detectado.**
- M2 EN, `en/channels/delete-channel.mdx:11` acrescido de "(excluded = true, soft delete)": a 4.1 detectou (`en/channels/delete-channel.mdx:11`). **Detectado.**
- M3 ES, exemplo do 502 revertido para `"error": 502, "message": "Hermitage deleteChannel failed"`: a checagem do 502 acusou `es`. **Detectado.**
- M4 EN, schema do 502 revertido de `InternalError` para `Error`: a checagem do 502 acusou `en`. **Detectado.**
- Pos-restauro: tudo zerado de novo; worktree removida; `git status --porcelain` igual a linha de base (vazio).
- Mutantes sobreviventes: nenhum.
- Limite do sensor: a 4.1 procura termos em lista fixa. Um vazamento com outra palavra ("marcado como removido", "inativo", "histórico preservado") nao seria detectado; conferi `preserv|registro|record` a mao, retorno vazio.

## Verificacoes adicionais

- (a) Escopo: 7 arquivos, todos esperados.
- (b) `docs.json` intocado.
- (c) 502 real `{"error":"Hermitage deleteChannel failed"}` (string, sem `message`) nos 3 OpenAPIs e no schema `InternalError`. Confirmado nas linhas citadas acima. Nao conferi contra a API nem contra o frisco; o corpo vem da spec.
- (d) Sem detalhes internos: greps de `lógic|logical|lógico|soft|excluded|preserv|registro|record` vazios nos 6 arquivos.
- (e) Paridade PT/EN/ES: mesma estrutura (conceituacao, condicoes, tabela de 5 status, aviso, erro 502, nota do `channelId`); linhas 11, 19, 33-39 equivalentes; os 3 OpenAPIs tem o mesmo `InternalError` e o mesmo exemplo.
- (f) Links: ver "Garantias tocadas".

## Quem rodou

- maquina: `verificar.mjs` em 2026-09-29 (worktree temporaria com so esta change)
- conferiu o resultado: o verificador (agente), que nao implementou a change
- sessao independente: verificador em sessão nova, sem o histórico da implementação

## Veredito

**APROVADO COM RESSALVAS**

Todos os 6 cenarios e os 3 requisitos tem evidencia `arquivo:linha` nos tres idiomas. Gate verde, sensor sem mutante sobrevivente.

Ressalvas:

1. Tarefa 4.4 (`mint dev`, conferir visualmente a secao nova e o painel do 502 nos 3 idiomas) segue aberta em `tasks.md:26`. Eu nao rodei o servidor: a renderizacao Mintlify nao foi verificada. Antes de arquivar, alguem precisa fazer isso.
2. Lacuna de precisao da spec: o cenario "Paridade entre idiomas" diz "o mesmo corpo de erro" sem dizer qual. Sugestao: dizer "o mesmo corpo do 502".
3. Questao em aberto do proposal, ainda valida: o corpo publico expoe o nome interno "Hermitage". A doc reproduz o que a API devolve; se o frisco tornar a mensagem generica, a doc muda junto.
4. `verificar.mjs` nao enxerga specs em `specs/<area>/<capacidade>/spec.md` e trava com varias changes ativas; a cobertura e a lista de impacto foram feitas a mao. Nenhuma correcao na change, so na ferramenta.
5. Esta verificacao nao conferiu o 502 contra a API real, apenas contra a spec.
