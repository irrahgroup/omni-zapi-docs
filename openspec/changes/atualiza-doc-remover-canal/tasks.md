# Tasks

## 1. Linha de base

- [x] 1.1 Confirmar que a doc nunca citou a carência de 40 dias: `grep -rnE "40 d|40 days|40 días|INSTANCE_WITHIN|graceDays" --include="*.mdx" --include="*.json" . | grep -v '^./openspec'` deve retornar vazio
- [x] 1.2 Registrar os textos a trocar: `grep -rniE "fisicamente|physically|físicamente|permanentemente|permanently" {channels,en/channels,es/channels}/delete-channel.mdx {pt,en,es}/channels/openapi-delete.json`
- [x] 1.3 Registrar o exemplo atual do `502` nos três OpenAPIs: `grep -n -A3 '"502"' {pt,en,es}/channels/openapi-delete.json`

## 2. Reescrever as páginas

- [x] 2.1 Reescrever a conceituação nas três `delete-channel.mdx` pelo efeito para o parceiro, sem "fisicamente", sem "permanentemente" e sem menção a exclusão lógica
- [x] 2.2 Acrescentar a condição de canal desconectado com `INSTANCE_STILL_CONNECTED` e o link para Desconectar canal, no prefixo de idioma de cada página (`/channels/`, `/en/channels/`, `/es/channels/`)
- [x] 2.3 Acrescentar a seção de erro `502` nas três páginas, com o mesmo conteúdo traduzido

## 3. Ajustar os OpenAPIs

- [x] 3.1 Reescrever a descrição do endpoint nos três `openapi-delete.json`, sem remoção física nem armazenamento interno
- [x] 3.2 Trocar o exemplo do `502` por `{ "error": "Hermitage deleteChannel failed" }` e apontar o schema para o novo `InternalError` (`error` como string), nos três idiomas
- [x] 3.3 Validar a integridade JSON: `python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('*/channels/openapi-delete.json')];print('ok')"`

## 4. Verificar

- [x] 4.1 Confirmar que nenhum termo interno vazou: `grep -rniE "lógic|logical|lógico|soft|excluded" {channels,en/channels,es/channels}/delete-channel.mdx {pt,en,es}/channels/openapi-delete.json` deve retornar vazio
- [x] 4.2 Confirmar o diff mínimo: `git diff --stat` lista só os 6 arquivos de "Impact", e `docs.json` fica intocado
- [x] 4.3 Rodar `python3 scripts/check-docs.py` e confirmar `check-docs: tudo certo`. Executado manualmente por quem implementa — este repositório não tem `.github/workflows/`, logo não há execução automática em PR
- [ ] 4.4 Subir `mint dev`, abrir `/channels/delete-channel` nos três idiomas e confirmar visualmente a seção nova e o exemplo do `502` no painel do endpoint; encerrar o servidor
