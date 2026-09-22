# Tasks

## 1. Linha de base

- [ ] 1.1 Registrar o estado inicial rodando `grep -rc "wamid" {pt,en,es}/messages/*.json | grep -v ':0'` e confirmar 30 ocorrências distribuídas em 30 arquivos
- [ ] 1.2 Confirmar que a string `wamid` não existe fora de `{pt,en,es}/messages/*.json`, rodando `grep -rl "wamid" --include="*.json" --include="*.mdx" . | grep -v "messages/"` e verificando saída vazia

## 2. Corrigir o valor de exemplo nos specs OpenAPI

- [ ] 2.1 Substituir `wamid.HBgNNTU0NDk3MDUwNzg1FQIAERgSM0` por `01A0C92D0C957FE98B73C8BA0CACF741` em `{pt,en,es}/messages/*.json`, com o comando escopado a esse caminho, e verificar que `grep -rc "wamid" {pt,en,es}/messages/` retorna 0 em todos os arquivos
- [ ] 2.2 Verificar que o diff é mínimo rodando `git diff --stat -- pt/messages en/messages es/messages` e confirmando 30 arquivos com exatamente 1 inserção e 1 remoção cada (nenhuma reformatação)
- [ ] 2.3 Confirmar que os três `openapi-template.json` (que declaram o `200` inline, não via `MessageSuccess`) foram alcançados, rodando `grep -n "01A0C92D" {pt,en,es}/messages/openapi-template.json`
- [ ] 2.4 Validar que os 30 arquivos continuam sendo JSON íntegro, rodando `python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('*/messages/*.json')];print('ok')"`

## 3. Declarar o formato na descrição do campo

- [ ] 3.1 Em `pt/messages/*.json`, atualizar a descrição de `MessageResponse.properties.messageId` de `ID da mensagem enviada` para `ID da mensagem enviada — hexadecimal de 32 caracteres maiúsculos`, e verificar com `grep -c "32 caracteres" pt/messages/*.json` retornando 1 por arquivo
- [ ] 3.2 Em `en/messages/*.json`, atualizar de `Sent message ID` para `Sent message ID — 32-character uppercase hexadecimal string`, verificando com `grep -c "32-character" en/messages/*.json`
- [ ] 3.3 Em `es/messages/*.json`, atualizar de `ID del mensaje enviado` para `ID del mensaje enviado — hexadecimal de 32 caracteres en mayúsculas`, verificando com `grep -c "32 caracteres" es/messages/*.json`
- [ ] 3.4 Revalidar a integridade JSON dos 30 arquivos com o mesmo comando da tarefa 2.4

## 4. Documentar a correlação com o webhook

- [ ] 4.1 Adicionar em `messages/introduction.mdx` (PT) uma seção `## Resposta da API` com o exemplo `{ "messageId": "01A0C92D0C957FE98B73C8BA0CACF741" }` e uma nota informando que esse valor é o mesmo entregue no webhook como `message._id`, com link para `/webhooks/payloads`; verificar que a página renderiza em `mint dev`
- [ ] 4.2 Adicionar a seção equivalente em `en/messages/introduction.mdx`, traduzida, mantendo o mesmo valor de exemplo e o mesmo link
- [ ] 4.3 Adicionar a seção equivalente em `es/messages/introduction.mdx`, traduzida, mantendo o mesmo valor de exemplo e o mesmo link
- [ ] 4.4 Conferir a paridade entre os três idiomas: `grep -c "01A0C92D0C957FE98B73C8BA0CACF741" messages/introduction.mdx en/messages/introduction.mdx es/messages/introduction.mdx` retorna 1 para cada

## 5. Verificação final

- [ ] 5.1 Confirmar que nenhum exemplo de resposta de envio contém `wamid`, rodando `grep -rn "wamid" . --include="*.json" --include="*.mdx"` e verificando saída vazia
- [ ] 5.2 Confirmar que a camada de compatibilidade Z-API ficou intacta: `git diff --stat -- pt/z-api en/z-api es/z-api z-api/` deve vir vazio, e `grep -c "D241XXXX732339502B68" pt/z-api/openapi.json` deve manter a contagem original
- [ ] 5.3 Confirmar que a seção de webhooks ficou intacta: `git diff --stat -- webhooks/ pt/webhooks/ en/webhooks/ es/webhooks/` deve vir vazio
- [ ] 5.4 Rodar `mint broken-links` e confirmar que os links adicionados na tarefa 4 resolvem
