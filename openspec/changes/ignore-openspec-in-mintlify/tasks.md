# Tasks

## 1. Reproduzir a falha

- [x] 1.1 Confirmar o estado quebrado rodando `mint broken-links` e registrar que ele aborta com `Syntax error - Unable to parse` apontando para um arquivo sob `openspec/`
- [x] 1.2 Confirmar que a causa é estrutural, verificando com `grep -rl -- "<!--" openspec --include="*.md"` que artefatos gerados pelos templates padrão contêm comentários HTML

## 2. Aplicar a exclusão

- [x] 2.1 Adicionar ao `.mintignore` uma seção com `openspec/` e um comentário curto explicando que são artefatos de planejamento, não documentação publicável; verificar com `grep -n "openspec" .mintignore`
- [x] 2.2 Verificar que o diff se limita a esse arquivo, rodando `git diff --stat` e confirmando que apenas `.mintignore` aparece

## 3. Verificar

- [x] 3.1 Rodar `mint broken-links` e confirmar que a execução completa até o relatório final, sem nenhum erro de parsing apontando para `openspec/`
- [x] 3.2 Confirmar que nenhuma página publicada saiu do alcance: o relatório deve continuar cobrindo as páginas da navegação do `docs.json`, e os achados remanescentes devem ser apenas os `{frontendUrl}` pré-existentes
- [x] 3.3 Confirmar que criar uma change nova não reintroduz a falha: rodar `mint broken-links` com a change atual (que já contém artefatos gerados pelos templates) presente no disco e verificar que completa
- [x] 3.4 Rodar `mint dev`, confirmar `✓ preview ready` e encerrar — garantindo que a exclusão não afetou o preview
