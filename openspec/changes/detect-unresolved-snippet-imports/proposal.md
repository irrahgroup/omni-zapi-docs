# Proposal

## Why

O `scripts/check-docs.py` retorna `tudo certo` mesmo com três páginas publicadas importando nomes que o snippet não exporta — o defeito tratado em `fix-z-api-snippet-imports`. O linter existe justamente para pegar esse tipo de coisa e não pegou.

São duas falhas independentes em `check_imports`:

**O regex de exportação ignora comentário.** Em `scripts/check-docs.py:162`, `re.findall(r'export const (\w+)', s)` roda sobre o arquivo cru. Um `export const` dentro de `{/* ... */}` casa do mesmo jeito, então `zapiBaseUrl` e `zapiOriginalUrl` entram no conjunto de nomes conhecidos como se estivessem disponíveis. Verificado: o regex devolve `True` para os dois.

**Falta a direção inversa.** O laço de `scripts/check-docs.py:176` percorre os nomes conhecidos e acusa "usa X sem import". Não existe a checagem oposta — "importa X que o snippet não exporta" —, que é a única capaz de pegar este caso.

As duas se combinam: mesmo corrigido o regex, sem a direção inversa o defeito continua invisível, porque o laço atual só olha para nomes que estão no conjunto.

## What Changes

- Descartar os blocos `{/* ... */}` antes de extrair os `export const`, para que o conjunto de nomes conhecidos reflita o que o MDX realmente exporta.
- Adicionar a checagem inversa: toda página que importa de um snippet deve importar apenas nomes que aquele snippet exporta; o que não existir vira erro com o arquivo e o nome.
- Manter a checagem atual de "usa sem import" e a de snippet inexistente, sem alteração de comportamento.

### Fora de escopo

- **Corrigir as três páginas quebradas**: é a change `fix-z-api-snippet-imports`. Esta aqui entrega só a detecção.
- **Acusar import não usado**: é ruído cosmético e não quebra build. Fica como ideia adiada, por decisão do autor da mudança, junto com o levantamento dos ~100 casos aparentes cuja contagem ainda não está estabelecida.

## Capabilities

### New Capabilities

- `tooling/docs-linting`: o que o linter de documentação do projeto precisa detectar. A change `ignore-openspec-in-mintlify` já introduz esta capacidade; enquanto nenhuma das duas for arquivada, `openspec/specs/` está vazio e as duas somam requisitos por `ADDED` no mesmo caminho.

### Modified Capabilities

<!-- Nenhuma: nenhuma das duas changes que tocam esta capacidade foi arquivada ainda, logo não há spec consolidada para modificar. -->

## Impact

**Arquivo alterado (1)**: `scripts/check-docs.py`, na função `check_imports` (linhas 158-179).

**Efeito imediato na base**: com a regra nova, o linter passa a **reprovar** enquanto `fix-z-api-snippet-imports` não entrar — são 6 violações, dois nomes em três arquivos. As duas changes precisam entrar juntas, ou a correção primeiro.

**Sem impacto**: páginas publicadas, snippets, `docs.json`, specs OpenAPI.

## Rastreabilidade

Sem task no ClickUp. Achado ao investigar por que o linter não pegou o defeito das páginas da Z-API. Precisa de task própria antes do PR — não pertence a HM-430.
