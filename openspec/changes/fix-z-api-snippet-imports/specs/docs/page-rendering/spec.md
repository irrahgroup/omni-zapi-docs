# Spec Delta

## Purpose

Define o contrato de integridade das páginas publicadas da documentação: o que cada página pode declarar como dependência de snippet e o que o build deve conseguir resolver sem emitir erro.

## ADDED Requirements

### Requirement: Toda página resolve os imports que declara

Uma página publicada SHALL importar de um snippet apenas nomes que aquele snippet exporta de fato. Um `export const` dentro de um bloco de comentário MDX (`{/* ... */}`) MUST NOT ser tratado como exportação disponível, porque o MDX não o expõe.

O build do preview MUST NOT emitir `Could not find export` para nenhuma página.

Fonte: `z-api/introduction.mdx:6` — linha de import da página de compatibilidade Z-API; `snippets/variables.mdx:13` — bloco `{/* ... */}` que contém os `export const zapiBaseUrl` e `zapiOriginalUrl` inativos.

#### Scenario: Página importa nome que o snippet não exporta

- **WHEN** uma página declara no import um nome que o snippet não exporta fora de comentário
- **THEN** isso é um defeito da página, a ser corrigido antes da publicação

#### Scenario: Build do preview das páginas da Z-API

- **WHEN** `mint dev` compila as três páginas de introdução da compatibilidade Z-API (PT, EN e ES)
- **THEN** nenhum erro `Could not find export` é emitido para `zapiBaseUrl` ou `zapiOriginalUrl`

#### Scenario: Import sem consumidor no corpo da página

- **WHEN** um nome importado não é usado no corpo da página e também não é exportado pelo snippet
- **THEN** o nome é removido do import, em vez de a exportação ser reativada no snippet

### Requirement: A correção preserva os imports em uso

A remoção de um import quebrado SHALL preservar, na mesma linha, todos os nomes que a página realmente usa, de modo que o conteúdo renderizado não mude.

Fonte: `z-api/introduction.mdx:6` — `projectName`, `frontendUrl` e `supportEmail` permanecem; `en/z-api/introduction.mdx:6` e `es/z-api/introduction.mdx:6` — mesma linha nas demais línguas.

#### Scenario: Conteúdo renderizado após a correção

- **WHEN** as três páginas são compiladas depois da remoção
- **THEN** `projectName`, `frontendUrl` e `supportEmail` continuam importados e resolvidos
- **AND** o texto renderizado de cada página é o mesmo de antes da correção
