# Tasks

## 1. Linha de base

- [x] 1.1 Registrar o estado inicial rodando `grep -rn "a1b2c3d4-e5f6-7890-abcd-ef1234567890" --include="*.json" .` e confirmar exatamente 6 ocorrências, em `openapi-create.json` e `openapi-connect.json` dos três idiomas
- [x] 1.2 Confirmar que o valor de destino já é o padrão da base, verificando com `grep -rc "019E4C54B1B375A28970B605CA9B03C3" --include="*.json" --include="*.mdx" .` que ele aparece em outros lugares como identificador de canal

## 2. Corrigir os exemplos

- [x] 2.1 Substituir o UUID pelo valor hexadecimal nos três `openapi-create.json`, com o comando escopado a `{pt,en,es}/channels/`, e verificar com `grep -n "019E4C54" {pt,en,es}/channels/openapi-create.json` que cada um tem a ocorrência na linha da resposta
- [x] 2.2 Substituir o UUID nos três `openapi-connect.json` e verificar com `grep -n "019E4C54" {pt,en,es}/channels/openapi-connect.json`
- [x] 2.3 Confirmar que nenhuma ocorrência do UUID sobrou em `channels/`, com `grep -rc "a1b2c3d4" {pt,en,es}/channels/` retornando 0 em todos os arquivos
- [x] 2.4 Verificar que o diff é mínimo: `git diff --numstat -- pt/channels en/channels es/channels` deve mostrar 6 arquivos com 1 inserção e 1 remoção cada
- [x] 2.5 Validar a integridade JSON dos 6 arquivos com `python3 -c "import json;[json.load(open(f)) for f in __import__('glob').glob('*/channels/openapi-*.json')];print('ok')"`

## 3. Verificar

- [x] 3.1 Confirmar que os UUIDs do CDN de figurinhas não foram tocados: `git diff --stat -- pt/messages en/messages es/messages` não deve conter `openapi-sticker.json`, e `grep -c "05bc83ea" {pt,en,es}/messages/openapi-sticker.json` deve manter a contagem original
- [x] 3.2 Confirmar que o spec órfão ficou intocado, com `git diff --stat -- "*openapi-create-channel.json"` vazio
- [x] 3.3 Subir `mint dev`, abrir `/channels/create-channel` e `/channels/connect-channel` e confirmar visualmente que os dois exibem o mesmo identificador hexadecimal; encerrar o servidor. Executado manualmente por quem implementa — este repositório não tem `.github/workflows/`, logo não há execução automática em PR
- [x] 3.4 Rodar `python3 scripts/check-docs.py` e confirmar `check-docs: tudo certo`. Também manual, pelo mesmo motivo
