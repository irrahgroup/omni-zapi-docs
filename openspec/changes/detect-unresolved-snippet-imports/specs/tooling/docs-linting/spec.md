# Spec Delta

## Purpose

Define o que a verificação automatizada de documentação do projeto precisa detectar e conseguir executar: quais defeitos o linter reprova, e qual é a fronteira entre os arquivos que as ferramentas do Mintlify devem processar e os diretórios de trabalho interno que devem ficar fora do alcance.

## ADDED Requirements

### Requirement: Exportação comentada não conta como disponível

Ao levantar o que um snippet exporta, o linter SHALL desconsiderar o conteúdo dos blocos de comentário MDX (`{/* ... */}`). Um `export const` dentro de um desses blocos MUST NOT entrar no conjunto de nomes disponíveis, porque o MDX não o expõe em tempo de build.

Fonte: `scripts/check-docs.py:162` — `check_imports`, onde `re.findall(r'export const (\w+)', s)` roda sobre o texto cru do snippet; `snippets/variables.mdx:13` — bloco `{/* ... */}` cujos `export const` são hoje contados como disponíveis.

#### Scenario: Snippet com exportação comentada

- **WHEN** um snippet contém `export const nome` dentro de um bloco `{/* ... */}`
- **THEN** `nome` não aparece entre os nomes que aquele snippet exporta
- **AND** uma página que o importe é tratada como importando um nome inexistente

#### Scenario: Exportação ativa permanece reconhecida

- **WHEN** um snippet contém `export const nome` fora de qualquer bloco de comentário
- **THEN** `nome` continua entre os nomes disponíveis, sem mudança no comportamento atual

### Requirement: Import de nome inexistente é reprovado

Para cada página que importa de um snippet, o linter SHALL verificar que todo nome da lista de import é exportado por aquele snippet. Um nome que não for exportado MUST produzir erro, identificando a página e o nome, e o processo MUST terminar com código de saída diferente de zero.

Fonte: `scripts/check-docs.py:176` — `check_imports`, laço `for name in known` que hoje cobre apenas a direção "usa sem import"; `scripts/check-docs.py:174` — `fail('import', ...)`, o canal de erro a ser reutilizado.

#### Scenario: Página importa nome que o snippet não exporta

- **WHEN** o linter roda sobre uma base em que uma página importa um nome ausente do snippet
- **THEN** reporta um erro nomeando a página e o nome
- **AND** termina com código de saída diferente de zero

#### Scenario: As páginas da Z-API no estado atual

- **WHEN** o linter roda antes da correção das três páginas de introdução da compatibilidade Z-API
- **THEN** reporta seis violações — `zapiBaseUrl` e `zapiOriginalUrl` em cada uma das três páginas

#### Scenario: Base sem import quebrado

- **WHEN** o linter roda sobre uma base em que toda página importa apenas nomes exportados
- **THEN** a regra nova não reporta nenhum erro

### Requirement: As checagens existentes seguem válidas

A adição das regras acima SHALL preservar o comportamento das checagens já existentes de import: a que acusa uso de um nome sem o import correspondente, e a que acusa import de um arquivo de snippet inexistente.

Fonte: `scripts/check-docs.py:179` — `fail('import', f'{f}: usa {name} sem import')`; `scripts/check-docs.py:174` — `fail('import', f'{f}: snippet inexistente ...')`.

#### Scenario: Uso sem import

- **WHEN** uma página usa um nome exportado por um snippet sem declarar o import
- **THEN** o linter continua reportando esse caso como erro

#### Scenario: Snippet inexistente

- **WHEN** uma página importa de um caminho de snippet que não existe no disco
- **THEN** o linter continua reportando esse caso como erro
