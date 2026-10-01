# Tasks

## 1. Reproduzir

- [ ] 1.1 Rodar `mint dev`, capturar o log e confirmar as duas linhas `Could not find export` para `zapiBaseUrl` e `zapiOriginalUrl`; encerrar o processo em seguida
- [ ] 1.2 Confirmar que os dois nomes não são usados no corpo das três páginas, rodando `grep -n "zapiBaseUrl\|zapiOriginalUrl" z-api/introduction.mdx en/z-api/introduction.mdx es/z-api/introduction.mdx` e verificando que só a linha 6 (o import) aparece em cada

## 2. Corrigir

- [ ] 2.1 Remover `zapiBaseUrl` e `zapiOriginalUrl` da linha de import de `z-api/introduction.mdx`, preservando os outros três nomes; verificar a linha resultante com `sed -n '6p'`
- [ ] 2.2 Aplicar a mesma remoção em `en/z-api/introduction.mdx`; verificar com `sed -n '6p'`
- [ ] 2.3 Aplicar a mesma remoção em `es/z-api/introduction.mdx`; verificar com `sed -n '6p'`
- [ ] 2.4 Confirmar que as três linhas ficaram idênticas entre si, comparando as saídas de `sed -n '6p'` dos três arquivos

## 3. Verificar

- [ ] 3.1 Rodar `mint dev` e confirmar `✓ preview ready` sem nenhum `Could not find export` no log; encerrar o processo. Executado manualmente por quem implementa — este repositório não tem `.github/workflows/`, logo não há execução automática em PR
- [ ] 3.2 Rodar `python3 scripts/check-docs.py` e confirmar `check-docs: tudo certo`. Também manual, pelo mesmo motivo
- [ ] 3.3 Confirmar que o conteúdo renderizado não mudou, verificando com `git diff` que o diff é de 3 linhas, uma por arquivo, todas na linha de import
- [ ] 3.4 Confirmar que `snippets/variables.mdx` não foi tocado, com `git diff --stat -- snippets/` vazio
