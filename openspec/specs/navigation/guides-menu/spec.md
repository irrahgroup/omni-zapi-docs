# navigation/guides-menu Specification

## Purpose
Define o estado e a ordem do grupo Canais no menu de guias e o destino do ícone de site no rodapé, para a navegação seguir o padrão dos demais grupos.

## Requirements

### Requirement: Grupo Canais aberto e sem botão de recolher

O grupo **Canais** da aba de guias SHALL aparecer expandido e sem o botão de recolher, como os demais grupos da aba, nos três idiomas. O grupo MUST NOT declarar `root` nem `directory` no `docs.json`.

Fonte: `docs.json:115` — grupo `Canais` da aba Guias pt-BR, hoje com `root: channels/overview` e `directory: card`, sem `expanded`; `docs.json:126` — grupo `Conectar canais`, que já é `expanded: true` e não tem `root`.

#### Scenario: Aberto e sem botão de recolher

- **WHEN** o leitor abre qualquer página dos guias, em qualquer idioma
- **THEN** o grupo Canais aparece aberto
- **AND** não há botão para recolhê-lo

#### Scenario: Configuração do grupo

- **WHEN** o `docs.json` é lido
- **THEN** o grupo Canais da aba Guias, nos três idiomas, tem `expanded: true` e não tem `root` nem `directory`

### Requirement: Ordem das páginas do grupo Canais

O grupo Canais SHALL listar as páginas na ordem Introdução, Visão geral dos canais e O que cada canal aceita, nos três idiomas.

Fonte: `docs.json:115` — páginas `channels/overview`, `channels/message-support`, `channels/introduction`, nesta ordem hoje; ordem desejada: `channels/introduction`, `channels/overview`, `channels/message-support`.

#### Scenario: Ordem

- **WHEN** o leitor abre o grupo Canais, em qualquer idioma
- **THEN** a primeira página é Introdução, depois Visão geral dos canais e O que cada canal aceita

#### Scenario: Links existentes

- **WHEN** a mudança é aplicada
- **THEN** as URLs das três páginas continuam as mesmas
- **AND** `python3 scripts/check-docs.py` termina com `check-docs: tudo certo`

### Requirement: Ícone de site do rodapé

O ícone de site do rodapé SHALL abrir `https://omni.z-api.io`.

Fonte: `docs.json:930` — `footer.socials.website`, hoje `https://www.omni.z-api.io`.

#### Scenario: Link do rodapé

- **WHEN** o leitor clica no ícone de site do rodapé, em qualquer idioma
- **THEN** o navegador abre `https://omni.z-api.io`
