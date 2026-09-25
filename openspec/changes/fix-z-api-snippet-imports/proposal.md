# Proposal

## Why

As três páginas de introdução da compatibilidade Z-API importam duas variáveis que o snippet não exporta. O Mintlify reclama a cada build do preview:

```
Error resolving import "zapiBaseUrl" in z-api/introduction.mdx: Could not find export zapiBaseUrl in snippet
Error resolving import "zapiOriginalUrl" in z-api/introduction.mdx: Could not find export zapiOriginalUrl in snippet
```

Os dois `export const` estão comentados em `snippets/variables.mdx:13-14`, dentro de um bloco `{/* ... */}`. Comentados desde o primeiro commit (`a3ff138`, 2026-09-07) — nunca chegaram a funcionar.

As duas variáveis **não são usadas** no corpo de nenhuma das três páginas: aparecem só na linha de import. O erro é ruído puro, sem efeito visível para o leitor, e mascara erros reais no log do `mint dev`.

## What Changes

- Remover `zapiBaseUrl` e `zapiOriginalUrl` da linha de import das três páginas de introdução da Z-API (PT/EN/ES), preservando `projectName`, `frontendUrl` e `supportEmail`, que são usados.
- Não descomentar os `export const`: as variáveis não têm consumidor, e reativá-las devolveria código morto ao snippet.

### Fora de escopo

- **Imports não usados de `projectName`, `frontendUrl` e `websiteUrl`** em outras páginas: são válidos (o nome existe no snippet) e não geram erro. A detecção que fiz é por regex e tem falso positivo provável em usos dentro de template literal, então o número real não está estabelecido. Ideia adiada, por decisão do autor da mudança.
- **A lacuna do linter que deixou isso passar**: change própria, `detect-unresolved-snippet-imports`, que adiciona a regra capaz de pegar este caso.

## Capabilities

### New Capabilities

- `docs/page-rendering`: contrato de integridade das páginas publicadas — toda página resolve os imports que declara, e o build não emite erro de import.

### Modified Capabilities

<!-- Nenhuma. -->

## Impact

**Arquivos alterados (3)**, uma linha cada:

- `z-api/introduction.mdx:6`, `en/z-api/introduction.mdx:6`, `es/z-api/introduction.mdx:6`.

**Sem impacto**: conteúdo renderizado das páginas (as variáveis não eram usadas), `snippets/variables.mdx`, specs OpenAPI, `docs.json`.

## Rastreabilidade

Sem task no ClickUp. Achado durante a verificação de `ignore-openspec-in-mintlify`, ao rodar `mint dev`. Precisa de task própria antes do PR — não pertence a HM-430, que trata do formato do `messageId`.
