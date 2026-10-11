# Tasks

## 1. Estabelecer o vermelho

- [ ] 1.1 Confirmar o falso "tudo certo" de hoje: rodar `python3 scripts/check-docs.py` com as três páginas da Z-API ainda quebradas e registrar que ele sai com código 0
- [ ] 1.2 Confirmar a causa da primeira falha, verificando que `re.findall(r'export const (\w+)', open('snippets/variables.mdx').read())` devolve `zapiBaseUrl` e `zapiOriginalUrl`, mesmo comentados

## 2. Corrigir o levantamento de exportações

- [ ] 2.1 Em `check_imports`, remover os blocos `{/* ... */}` do texto do snippet antes de extrair os `export const`; verificar que `zapiBaseUrl` e `zapiOriginalUrl` deixam de constar entre os nomes conhecidos
- [ ] 2.2 Confirmar que nenhuma exportação ativa foi perdida, comparando o conjunto de nomes conhecidos antes e depois — a diferença deve ser exatamente os dois nomes comentados

## 3. Adicionar a checagem inversa

- [ ] 3.1 Em `check_imports`, para cada import de página, acusar por `fail('import', ...)` todo nome que o snippet de origem não exporta, nomeando página e nome
- [ ] 3.2 Confirmar que a regra pega o caso real: rodar o linter com as três páginas ainda quebradas e verificar que reporta as seis violações e sai com código diferente de zero
- [ ] 3.3 Confirmar que a regra não é cega: corrigir temporariamente uma das três páginas, rodar de novo, verificar que passam a ser quatro violações, e desfazer a correção temporária

## 4. Verificar

- [ ] 4.1 Confirmar que as checagens antigas seguem vivas: introduzir temporariamente uma página que usa um nome sem import, verificar que o linter acusa, e desfazer
- [ ] 4.2 Confirmar o mesmo para snippet inexistente: apontar temporariamente um import para um caminho que não existe, verificar que o linter acusa, e desfazer
- [ ] 4.3 Rodar `python3 scripts/check-docs.py` depois que `fix-z-api-snippet-imports` estiver aplicada e confirmar `check-docs: tudo certo` com código 0. Executado manualmente por quem implementa — este repositório não tem `.github/workflows/`, logo não há execução automática em PR
- [ ] 4.4 Confirmar que o diff se limita a `scripts/check-docs.py`, com `git diff --stat`
