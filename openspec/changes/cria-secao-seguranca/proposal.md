# Proposal

## Why

O painel e a API do Omni Z-API já têm cinco recursos de segurança: restrição de IP, domínios autorizados da SDK, autenticação de dois fatores, time e papéis, e auditoria. A documentação não tem nenhuma página sobre eles. O cliente não sabe como configurar cada recurso, o que ganha com ele, que limites ele tem e o que a API responde quando recusa uma chamada por regra de segurança.

O conteúdo do Z-API clássico não serve de base. Lá a autenticação é por instância; no Omni Z-API ela é por workspace, com **Public Key** e **Secret Key** em `Authorization: Bearer <chave>`.

Durante a revisão também apareceram dois defeitos de navegação. O grupo **Canais** do menu fica fechado e põe **Introdução** por último. O ícone de site do rodapé aponta para `https://www.omni.z-api.io`, e não para `https://omni.z-api.io`.

## What Changes

- Novo grupo **Segurança** / **Security** / **Seguridad** na aba de guias dos três idiomas, com seis páginas: Introdução, Restrição de IP, Domínios da SDK, 2FA, Time e papéis e Auditoria.
- A **Introdução** diz onde cada recurso fica no painel, o que ele protege e quem pode configurá-lo.
- A **Restrição de IP** documenta o comportamento medido no `pennsylvania-frisco`: lista vazia libera qualquer IP; com a lista preenchida, só os IPs cadastrados chamam rotas autenticadas por Secret Key; a comparação é exata; não há CIDR; `X-Forwarded-For` é ignorado; a mudança leva até 10 minutos para valer; o bloqueio responde `400` com `{"error": "<ip> not allowed"}` ou `{"error": "ip not allowed"}`.
- A página **Domínios da SDK** ensina a cadastrar a **origem exata** e explica que o painel do Omni é sempre aceito. A página **não** promete curinga: a SDK compara a origem exata, e `*.example.com` nunca casa (ver Questão em aberto).
- A página **2FA** ensina a ativar o recurso. Ela deixa claro que o 2FA protege o login no painel e não muda a autenticação da API.
- A página **Time e papéis** traz a tabela de permissões de Owner, Manager e Membro e explica o convite, o aceite (quem aceita entra como Membro) e a promoção ou o rebaixamento.
- A página **Auditoria** explica quem acessa o log, os tipos de registro, os filtros, o resultado e o detalhe de cada evento e a exportação CSV. Ela diz que os registros não podem ser alterados e **não** cita prazo de retenção enquanto produto não o decidir (ver Questões em aberto).
- O grupo **Canais** do menu passa a ficar aberto e **sem o botão de recolher**, como os outros grupos, na ordem Introdução → Visão geral dos canais → O que cada canal aceita. Para isso o grupo perde `root` e `directory` no `docs.json`, e não basta `expanded: true`.
- O link de site do rodapé passa a ser `https://omni.z-api.io`.
- Nenhuma mudança quebra compatibilidade. A change só documenta comportamento que já existe e corrige a navegação.

### Fora de escopo

- **Curinga em domínios da SDK.** O painel sugere `*.example.com` (`pennsylvania-lancaster` `src/i18n/pt-br.json:1718`, `security.sdk.domainsDescription`), mas a SDK compara a origem exata (`pennsylvania-lester` branch `omnizapi`, `src/core/client.ts:416`). A divergência é um bug do produto e precisa ser resolvida no painel ou na SDK. Por decisão do autor, esta change documenta só o que a SDK faz hoje.
- **Credenciais (Public Key e Secret Key) e Meta App.** Os dois ficam na mesma tela de Segurança do painel, mas a task não os pede. As credenciais já estão em `authentication.mdx`. A Introdução só aponta para essa página.
- **Permissões avulsas por membro** (extras além do papel), previstas no desenho da hermitage (`docs/user-permissions-plan.md`). A task pede os três papéis, e o painel não expõe concessão avulsa nas telas medidas.
- **Prazo de retenção do log de auditoria.** O texto do painel diz "últimos 13 meses" (`pennsylvania-lancaster@ominizapi` `src/i18n/pt-br.json:309`), mas o código do `pennsylvania-hermitage` não aplica esse prazo: `git grep -n -i "plusMonths(13)\|minusMonths(13)\|RETENTION" origin/develop -- src/main` só acha `PruneAuditOutboxService.RETENTION` de 7 dias, que é a fila de saída. `EnsureAuditPartitionsService` só cria partições (`MONTHS_AHEAD = 2`), nenhum job apaga as antigas e a busca usa só o `dateFrom` e o `dateTo` do filtro. O único prazo achado é `ListAuditActionsService.LOOKBACK` de 90 dias, que só limita a lista de ações do filtro. A página diz que os registros não podem ser alterados e não cita prazo nenhum até a decisão, nem 13 meses nem "sem prazo".
- **Rota de compatibilidade Z-API** (`pennsylvania-reading`) na página de IP. A página fala só da API do Omni (`pennsylvania-frisco`).
- **Ferramentas de staff** (auditoria por admin, remover 2FA de outro usuário). São internas da Irrah e não aparecem para o cliente.
- **2FA de instância Mobile** (`instances.deviceDetails...2Factor`). É o PIN do WhatsApp e não tem relação com o login no painel.
- **Endpoints de API para gerir IP, domínios, papéis ou auditoria.** Hoje eles só aceitam sessão do painel (`!hasAnyAuthority('ALLOW_INTEGRATION')`), então nada vira referência de API.

## Capabilities

### New Capabilities

- `security/security-section`: existência, posição e conteúdo introdutório da seção Segurança nos três idiomas.
- `security/ip-restriction`: o que a documentação promete sobre a lista de IPs e a recusa de chamadas por IP.
- `security/sdk-authorized-domains`: o que a documentação promete sobre os domínios onde a SDK de conexão pode abrir.
- `security/two-factor-authentication`: ativação e escopo do 2FA de login no painel.
- `security/team-roles`: papéis do workspace, permissões de cada um, convite e troca de papel.
- `security/audit-log`: acesso, conteúdo, filtros, exportação do log de auditoria e a regra de não citar retenção até a confirmação.
- `navigation/guides-menu`: estado e ordem do grupo Canais no menu de guias e o link de site do rodapé.

### Modified Capabilities

<!-- Nenhuma: `openspec/specs/` ainda não tem capacidade consolidada. -->

## Impact

**Arquivos novos (18):** `{,en/,es/}security/{introduction,ip-restriction,sdk-domains,two-factor,team,audit}.mdx`.

**Arquivos alterados (1):** `docs.json`. Ele recebe o novo grupo nos três idiomas, a mudança do grupo Canais (aberto, sem `root` nem `directory`) nos três idiomas e o `footer.socials.website`.

**Sem impacto:** OpenAPIs, páginas de referência de API, aba Compatibilidade Z-API, `snippets/variables.mdx` (`websiteUrl` continua igual; ver design).

## Questões em aberto

**Retenção da auditoria.** O código não aplica os 13 meses que o painel promete. **Decisão de produto.** A página só cita um prazo depois que produto decidir qual vale e como ele passa a ser aplicado (apagar partições antigas, limitar a consulta ou corrigir o texto do painel). Com a decisão, a página e a spec `security/audit-log` ganham o número.

**Curinga na SDK.** O painel diz "Use *.example.com para wildcard", e a SDK não aceita curinga. Quem mantém o `pennsylvania-lancaster` e o `pennsylvania-lester` precisa decidir entre implementar o curinga na SDK ou tirar a dica do painel. Se o curinga for implementado, a página de Domínios da SDK muda junto.

## Rastreabilidade

ClickUp **HM-480**: *Criar seção Segurança na documentação do Z-API Omni*. A task é só de documentação e cabe inteira neste repositório.

```
branch   HM-480-proposta-secao-seguranca
título   docs(HM-480): propõe a seção Segurança
change   cria-secao-seguranca
```
