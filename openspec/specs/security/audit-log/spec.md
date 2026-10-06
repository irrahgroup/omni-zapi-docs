# security/audit-log Specification

## Purpose
Define o que a documentação promete sobre o log de auditoria do workspace: quem acessa, o que ele registra, como filtrar, exportar e, depois de confirmado, por quanto tempo os registros ficam disponíveis.

## Requirements

### Requirement: Acesso ao log

A página Auditoria SHALL informar que Owner e Manager acessam o log e que Membro não acessa. A página SHALL informar que o log aparece só no painel e não tem endpoint para chamada com chave de API.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/entrypoint/http/audit/AuditEventResource.java:42` — `WS_VIEW_AUDIT` e `!ALLOW_INTEGRATION`; `src/main/java/com/irrahtech/nebraska/lincoln/core/domain/workspace/MembershipRole.java:19` — Manager tem `WS_VIEW_AUDIT`, Membro não.

#### Scenario: Quem acessa

- **WHEN** o leitor consulta quem acessa
- **THEN** a página diz que Owner e Manager acessam e que Membro não

### Requirement: Conteúdo do registro

A página SHALL listar o que cada evento traz: data, autor (usuário, integração ou sistema), ação, recurso afetado, resultado (**Sucesso**, **Falha** ou **Negado**) e IP. A página SHALL listar os tipos de recurso (canal, webhook, template, workspace, usuário, membro, convite, faturamento, assinatura, credenciais, sessão) e o detalhe do evento. A página SHALL dizer que um registro não pode ser alterado.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` chaves `audit.table.*`, `audit.detail.*`, `audit.outcome.*`, `audit.actor.*`, `audit.resource.*`, `audit.verb.*`; `src/i18n/pt-br.json:309` — "Logs imutáveis".

#### Scenario: Colunas e resultado

- **WHEN** o leitor consulta o conteúdo do registro
- **THEN** vê as colunas e os três resultados possíveis, com o significado de cada um

#### Scenario: Detalhe do evento

- **WHEN** o leitor consulta o detalhe
- **THEN** vê os campos de quem fez, o que foi afetado e da requisição, sem prometer campo que a tela não mostra

### Requirement: Filtros e escopo de visualização

A página SHALL listar os filtros: ação, tipo de autor, resultado, login do autor, período (de/até) e tipo de recurso. A página SHALL explicar a escolha entre ver o workspace todo e ver só as próprias ações.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` chaves `audit.filters.*` e `audit.scope.*`.

#### Scenario: Filtros

- **WHEN** o leitor consulta os filtros
- **THEN** vê os seis filtros e os botões de aplicar e limpar

#### Scenario: Escopo

- **WHEN** o leitor consulta o escopo
- **THEN** a página diz o que cada opção mostra

### Requirement: Exportação CSV

A página SHALL explicar a exportação em CSV.

Fonte (`pennsylvania-lancaster@ominizapi`): `src/i18n/pt-br.json` chave `audit.actions.exportCsv`; `src/pages/app/security/audit-log/index.tsx` — exportação.

#### Scenario: Exportar

- **WHEN** o leitor consulta a exportação
- **THEN** a página diz como exportar o resultado dos filtros atuais e o que acontece quando não há nada a exportar

### Requirement: Retenção só depois de confirmada

A página MUST NOT citar prazo de retenção dos registros enquanto produto não decidir o prazo e ele não estar aplicado no código. O texto do painel ("últimos 13 meses") não basta como fonte: o código do `pennsylvania-hermitage` não aplica esse prazo, nem para apagar registros antigos nem para limitar a consulta. A página também MUST NOT afirmar que os registros são guardados sem prazo. A página SHALL dizer que os registros não podem ser alterados.

Fonte (`pennsylvania-hermitage@develop`): `git grep -n -i "plusMonths(13)\|minusMonths(13)\|RETENTION" origin/develop -- src/main` só encontra `PruneAuditOutboxService.java:14` — `PruneAuditOutboxService.RETENTION`, de 7 dias, que vale para a fila de saída. No `pennsylvania-hermitage@develop`: `EnsureAuditPartitionsService.java:14` — `MONTHS_AHEAD = 2`, o serviço só cria partições futuras de `audit_event`; `git grep -n -i -E 'drop (table|partition)|detach' origin/develop -- src/main` só acha `DROP TABLE` de migrations antigas de outras tabelas, ou seja, nenhum job apaga partições antigas; `QueryAuditEventRepositoryProvider.java:87` e `:90` — a busca filtra só pelo `dateFrom` e `dateTo` informados, sem limite de 13 meses; `V29__create_audit_event.sql:2` — a tabela é particionada por mês e imutável (`audit_event_block_change`); `ListAuditActionsService.java:14` — `ListAuditActionsService.LOOKBACK` = 90 dias, o único prazo no fluxo de auditoria além da fila de saída, e ele só limita a lista de ações oferecida no filtro, não os registros. Fonte do texto do painel: `pennsylvania-lancaster@ominizapi` `src/i18n/pt-br.json:309`.

#### Scenario: Prazo ainda não confirmado

- **WHEN** o leitor abre a página Auditoria
- **THEN** a página não contém "13 meses", "13 months" nem "13 meses" em espanhol, nem outro prazo de retenção
- **AND** a página diz que os registros não podem ser alterados

#### Scenario: Prazo confirmado depois

- **WHEN** produto decidir o prazo, e ele estiver aplicado no código, e a página for atualizada
- **THEN** o prazo entra nas três versões, com a fonte do código ou da confirmação
