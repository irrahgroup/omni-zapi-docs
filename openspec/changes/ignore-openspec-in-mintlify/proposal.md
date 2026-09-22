# Proposal

## Why

O Mintlify varre todo arquivo `.md`/`.mdx` do projeto, e os artefatos de planejamento do OpenSpec em `openspec/changes/**/*.md` usam comentários HTML (`<!-- ... -->`) — sintaxe que o MDX rejeita. Com isso, `mint broken-links` aborta:

```
erro Syntax error - Unable to parse
    openspec/changes/<change>/proposal.md - 29:2: Unexpected character `!` (U+0021)
```

A falha é estrutural, não pontual: os templates que o `openspec instructions` entrega para `proposal.md`, `specs/**/spec.md` e `tasks.md` contêm 5, 6 e 6 comentários HTML respectivamente, e quem escreve o artefato os herda. Toda change nova quebra o comando de novo.

O impacto está confinado ao `mint broken-links`. `mint dev` sobe normalmente — verificado nesta investigação.

## What Changes

- Adicionar `openspec/` ao `.mintignore`, com um comentário curto explicando que são artefatos de planejamento e não documentação publicável.
- Nenhum arquivo de documentação é alterado; nenhuma rota do `docs.json` é afetada.

### Fora de escopo

- **`.gitignore`**: `openspec/` está untracked hoje. Se o time decidir versionar os artefatos de planejamento, essa escolha é independente desta correção — o `.mintignore` é necessário nos dois casos, porque o Mintlify lê o disco, não o índice do git.
- **Os 21 links `{frontendUrl}` reportados como quebrados**: falso positivo pré-existente do checker, que não resolve variáveis de snippet em `href`. Investigação e correção próprias.
- **Imports quebrados em `z-api/introduction.mdx`** (PT/EN/ES): as três páginas importam `zapiBaseUrl` e `zapiOriginalUrl`, que estão comentados em `snippets/variables.mdx:13-14`. Bug real, sem relação com este, e merece change própria.

## Capabilities

### New Capabilities

- `tooling/docs-linting`: define o que a verificação de documentação do projeto deve conseguir rodar, e quais diretórios ficam fora do alcance do Mintlify por não serem documentação publicável.

### Modified Capabilities

<!-- Nenhuma. -->

## Impact

**Arquivo alterado (1)**: `.mintignore` — uma entrada nova.

**Verificação destravada**: `mint broken-links` volta a completar a execução, deixando de abortar no primeiro artefato de planejamento. Isso é pré-requisito para qualquer checagem de links em CI ou em revisão local.

**Sem impacto**: páginas publicadas, `docs.json`, snippets, specs OpenAPI, `mint dev`.
