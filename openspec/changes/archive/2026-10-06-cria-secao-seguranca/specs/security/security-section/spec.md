# Spec Delta

## Purpose

Define a existência, a posição e o conteúdo introdutório da seção Segurança da documentação do Omni Z-API, nos três idiomas, para que o cliente saiba quais proteções existem, onde configurá-las e o que cada uma entrega.

## ADDED Requirements

### Requirement: Seção Segurança no menu de guias

O menu da aba de guias SHALL ter o grupo **Segurança** (`Security` em inglês, `Seguridad` em espanhol) com seis páginas, nesta ordem: Introdução, Restrição de IP, Domínios da SDK, Autenticação de dois fatores, Time e papéis e Auditoria. Cada idioma MUST ter o mesmo conjunto de páginas.

Fonte: `docs.json:139` — grupo `Conceitos do WhatsApp`, junto ao qual o novo grupo entra na aba Guias pt-BR.

#### Scenario: Menu em português

- **WHEN** o leitor abre a aba **Guias** em português
- **THEN** existe o grupo **Segurança** com as seis páginas na ordem definida

#### Scenario: Paridade entre idiomas

- **WHEN** o leitor troca para inglês ou espanhol
- **THEN** o grupo traz as mesmas seis páginas, com título e descrição traduzidos
- **AND** `python3 scripts/check-docs.py` termina com `check-docs: tudo certo`

### Requirement: Introdução explica local e benefício de cada recurso

A página Introdução SHALL dizer, para cada um dos cinco recursos (IP, domínios da SDK, 2FA, time e papéis, auditoria), onde ele fica no painel, o que o cliente ganha com ele e quem pode configurá-lo. A página MUST apontar para a página de cada recurso.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json:309` — título e subtítulo de Auditoria; `src/i18n/pt-br.json:1718` — texto de domínios da SDK; `src/i18n/pt-br.json` chave `security.ipDescription` — descrição de restrição de IP.

#### Scenario: Visão geral dos recursos

- **WHEN** o leitor abre a Introdução
- **THEN** vê os cinco recursos, cada um com a localização no painel e o benefício em uma ou duas frases
- **AND** cada recurso tem link para a sua página

#### Scenario: Escopo das proteções

- **WHEN** o leitor consulta a Introdução
- **THEN** a página informa que a API autentica por workspace com Public Key e Secret Key em `Authorization: Bearer <chave>`
- **AND** a página não descreve autenticação por instância
