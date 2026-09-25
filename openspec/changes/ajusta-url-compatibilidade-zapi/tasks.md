# Tasks

## 1. Linha de base

- [x] 1.1 Registrar as 15 ocorrências alvo com `grep -rn "api\.omni\.z-api\.io" --include="*.json" --include="*.mdx" . | grep "z-api/"` e confirmar 9 arquivos
- [x] 1.2 Registrar a contagem da API unificada, que não deve mudar: `grep -ro "api\.omni\.z-api\.io" --include="*.json" --include="*.mdx" . | grep -v "z-api/" | wc -l` deve dar 79

## 2. Trocar o host

- [x] 2.1 Substituir `api.omni.z-api.io` por `zapi.omni.z-api.io` nos três `openapi.json` de compatibilidade e verificar o `servers[0].url` de cada um com `python3 -c "import json;print(json.load(open(f))['servers'])"`
- [x] 2.2 Substituir nas três `z-api/introduction.mdx` e verificar com `sed -n '22p;49p;86p'` que a tabela, o `curl` e o texto de migração apontam para o host novo
- [x] 2.3 Substituir nas três `z-api/authentication.mdx` e verificar a linha 51 de cada
- [x] 2.4 Confirmar que nenhuma ocorrência do host antigo sobrou em `*/z-api/`, com `grep -rc "api\.omni\.z-api\.io" */z-api z-api` retornando 0

## 3. Verificar o que não podia mudar

- [x] 3.1 Confirmar que a API unificada continua intacta: a contagem fora de `*/z-api/` segue 79, e `git diff --stat` não lista nenhum arquivo de `messages/`, `channels/`, `webhooks/` ou `templates/`
- [x] 3.2 Confirmar que `api.z-api.io` foi preservado: `grep -rc "https://api\.z-api\.io" */z-api z-api` mantém a contagem original, e o lado esquerdo das tabelas de comparação segue apontando para a Z-API original
- [x] 3.3 Validar a integridade JSON dos três `openapi.json` de compatibilidade
- [x] 3.4 Rodar `python3 scripts/check-docs.py` e confirmar `check-docs: tudo certo`. Executado manualmente por quem implementa — este repositório não tem `.github/workflows/`, logo não há execução automática em PR
- [x] 3.5 Subir `mint dev`, abrir a introdução da compatibilidade e confirmar visualmente o host novo na tabela e no `curl`; encerrar o servidor
