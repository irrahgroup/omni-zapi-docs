# Spec Delta

## Purpose

Define o que a verificação automatizada de documentação do projeto precisa detectar e conseguir executar: quais defeitos o linter reprova, e qual é a fronteira entre os arquivos que as ferramentas do Mintlify devem processar e os diretórios de trabalho interno que devem ficar fora do alcance.

## ADDED Requirements

### Requirement: A verificação de links deve completar a execução

O comando de verificação de links da documentação SHALL processar todas as páginas publicáveis e chegar ao fim, reportando seus achados. Ele MUST NOT abortar por causa de arquivos que não são documentação publicável.

#### Scenario: Artefatos de planejamento presentes no diretório de trabalho

- **WHEN** o repositório contém artefatos de planejamento do OpenSpec em `openspec/`
- **THEN** `mint broken-links` completa a execução e reporta seus achados
- **AND** nenhum erro de parsing aponta para um arquivo sob `openspec/`

#### Scenario: Uma change nova é criada

- **WHEN** uma change nova produz artefatos a partir dos templates padrão, que contêm comentários HTML
- **THEN** a verificação de links continua completando a execução, sem necessidade de ajuste manual

### Requirement: Somente documentação publicável é processada pelo Mintlify

O `.mintignore` SHALL excluir os diretórios de trabalho interno que contêm arquivos `.md` não destinados à publicação, de modo que o alcance do Mintlify corresponda ao conjunto de páginas efetivamente servidas.

#### Scenario: Diretório de planejamento

- **WHEN** um colaborador inspeciona o `.mintignore`
- **THEN** encontra `openspec/` listado, acompanhado da razão pela qual está ali

#### Scenario: Páginas publicadas permanecem no alcance

- **WHEN** a verificação roda após a exclusão
- **THEN** todas as páginas referenciadas na navegação do `docs.json` continuam sendo processadas
- **AND** nenhuma página publicada deixa de ser verificada
