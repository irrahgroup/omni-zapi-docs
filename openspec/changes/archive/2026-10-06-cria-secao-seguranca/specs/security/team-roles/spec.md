# Spec Delta

## Purpose

Define o que a documentação promete sobre os papéis do workspace (Owner, Manager e Membro), as permissões de cada um e o fluxo de convite e troca de papel.

## ADDED Requirements

### Requirement: Permissões de cada papel

A página Time e papéis SHALL trazer uma tabela com o que Owner, Manager e Membro podem fazer, por área: canais, templates, membros, papéis, faturamento, auditoria e configurações do workspace (IP e domínios da SDK). Owner SHALL ter todas as permissões. Manager SHALL ver e gerir canais, templates e membros e SHALL ver faturamento e auditoria, mas não gerir papéis, faturamento nem configurações do workspace. Membro SHALL só ver canais e templates.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/core/domain/workspace/MembershipRole.java:16` — `MembershipRole.basePermissions`.

#### Scenario: Tabela de permissões

- **WHEN** o leitor abre a tabela
- **THEN** cada papel aparece com as permissões acima, sem permissão a mais nem a menos

#### Scenario: Auditoria por papel

- **WHEN** o leitor consulta a linha de auditoria
- **THEN** Owner e Manager aparecem com acesso e Membro aparece sem acesso

### Requirement: Convite e aceite

A página SHALL explicar como convidar pessoas por e-mail (um ou vários, separados por vírgula), que o convite expira em 7 dias, que pode ser reenviado ou revogado e que quem aceita entra como **Membro**.

Fonte (`pennsylvania-hermitage@develop`): `src/main/java/com/irrahtech/nebraska/lincoln/core/domain/workspace/WorkspaceInvitation.java:27` — `WorkspaceInvitation.EXPIRATION_MINUTES` = `7 * 24 * 60`, ou seja, 7 dias. Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/core/usecase/interactor/workspace/AcceptInvitationInteractor.java:76` — `AcceptInvitationInteractor`, papel inicial `MEMBER`; `src/main/java/com/irrahtech/nebraska/lincoln/core/usecase/interactor/workspace/InviteMemberInteractor.java:82` — `InviteMemberInteractor`, grava a expiração do convite.

#### Scenario: Convidar

- **WHEN** o leitor segue o passo a passo de convite
- **THEN** encontra o caminho no painel, o campo de e-mails, a revisão e o envio

#### Scenario: Aceite

- **WHEN** o leitor consulta o que acontece após o aceite
- **THEN** a página diz que a pessoa entra como Membro, quaisquer que sejam os papéis de quem convidou

### Requirement: Promoção e rebaixamento

A página SHALL explicar que o Owner promove Membro a Manager e rebaixa Manager a Membro. A página SHALL dizer que não se atribui o papel Owner por essa tela, que ninguém altera o próprio papel e que o Owner não é alvo de remoção nem de troca. A página SHALL dizer que o Manager só gere Membros.

Fonte (`pennsylvania-hermitage@main`): `src/main/java/com/irrahtech/nebraska/lincoln/core/usecase/service/workspace/WorkspaceAuthorizationService.java:48` — `requireRoleChange`; `:77` — `validateRequestedRole`; `:34` — `requireMemberTarget`; `:106` — `rejectOwnerTarget`.

#### Scenario: Promover e rebaixar

- **WHEN** o leitor consulta a gestão de papéis
- **THEN** encontra como promover Membro a Manager e rebaixar Manager a Membro, e que só o Owner faz isso

#### Scenario: Limites

- **WHEN** o leitor consulta os limites
- **THEN** a página diz que não há troca para Owner, que ninguém muda o próprio papel e que o Manager só gere Membros
