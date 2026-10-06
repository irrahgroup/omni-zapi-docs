# Design

## Context

O repositório é um site Mintlify. Cada página existe em três árvores: `pt` na raiz (`channels/...`), `en/` e `es/`. O `docs.json` declara o menu de cada idioma e `scripts/check-docs.py` confere a paridade entre eles. O repositório não tem `.github/workflows/` (conferido com `ls .github` na raiz de `docs-omni`, que retorna "No such file or directory"), então nenhuma verificação roda sozinha em PR.

O conteúdo vem de código de outros repositórios, lido na branch indicada em cada `Fonte:` das specs:

- `pennsylvania-frisco@develop`: a API pública do Omni. Ela aplica a lista de IPs em rotas de Secret Key e monta o `sdk-info`.
- `pennsylvania-hermitage@main`: papéis, convites, auditoria e gravação de IP e domínios.
- `pennsylvania-lancaster@ominizapi`: o painel. Dele vêm os textos e os fluxos das telas.
- `pennsylvania-lester@omnizapi`: a SDK de conexão.
- `pennsylvania-reading@develop`: a rota de compatibilidade Z-API.

`frisco` na `develop` e na `main` tem o mesmo comportamento de IP (cache de 10 minutos, comparação exata). O `reading` difere entre as duas (ver D3).

## Goals / Non-Goals

**Goals:**

- Seis páginas novas por idioma, com o comportamento real do produto.
- Grupo Canais aberto e com Introdução primeiro; link de rodapé correto.
- Todas as afirmações com procedência no código, e nenhuma delas copiada do Z-API clássico.

**Non-Goals:**

- Corrigir o curinga do painel ou da SDK (Questão em aberto da proposta).
- Mudar OpenAPIs, `snippets/variables.mdx` ou a aba Compatibilidade Z-API.
- Documentar credenciais, Meta App ou permissões avulsas.

## Decisions

**D1. Seção no grupo de guias, e não na referência da API.** Os cinco recursos são do painel. Os endpoints que os sustentam só aceitam sessão de usuário (`!hasAnyAuthority('ALLOW_INTEGRATION')`), então um cliente de API nunca os chama. Por isso o grupo entra na aba **Guias**, entre **Conceitos do WhatsApp** e **Configurar a Meta**, e fica `expanded: true` como **Começar** e **Conectar canais**. O grupo **Canais** passa a seguir o mesmo padrão: `expanded: true` e sem `root` nem `directory`. Só `expanded: true` não tira o botão de recolher, e o `root` com `directory: card` faz do título do grupo um link para a visão geral. Sem eles, `channels/overview` vira uma página comum da lista, na ordem pedida. A alternativa, uma aba própria, foi descartada: seis páginas não justificam uma aba nova.

**D2. Nomes de arquivo iguais nos três idiomas.** `security/introduction`, `security/ip-restriction`, `security/sdk-domains`, `security/two-factor`, `security/team`, `security/audit`. Assim o `check-docs.py` consegue comparar os idiomas pelo caminho. Em `en/` e `es/` o caminho ganha o prefixo do idioma, como nas demais páginas.

**D3. A Restrição de IP descreve o comportamento da API do Omni, sem citar a rota de compatibilidade.** Os textos de bloqueio do `frisco` são `<ip> not allowed` e `ip not allowed`. O `reading` na `develop` devolve `remote IP not allowed` quando não identifica o IP, e na `main` ainda confia em `CF-Connecting-IP`, aceita lista de IPs com cache de 10 dias e ignora a regra se o IP vier vazio. Documentar as duas versões confundiria o leitor. A página fala só do que o `frisco` faz. A aba **Compatibilidade Z-API** fica fora, e a diferença vai como pendência na task.

**D4. Papéis em tabela, com as permissões por área e não por nome de permissão.** O código tem 11 permissões `WS_*`. O cliente enxerga áreas (canais, templates, membros, papéis, faturamento, auditoria, configurações do workspace), então a tabela usa essas áreas. A fonte de cada linha é `MembershipRole.basePermissions`.

**D5. Domínios da SDK: só origem exata.** Decidido pelo autor na revisão: o texto segue a SDK e não a dica do painel. A página diz expressamente que cada subdomínio precisa de cadastro próprio. Se o curinga passar a existir, uma change nova atualiza a página.

**D6. Rodapé: só `docs.json`.** `websiteUrl` em `snippets/variables.mdx` é usado em `index.mdx` e em outros textos, e a task só pede o ícone do rodapé. Mudar a variável alteraria páginas fora do escopo.

**D8. Retenção da auditoria fica fora da página até ser confirmada.** O prazo só existe no texto do painel (`src/i18n/pt-br.json:309`). No `pennsylvania-hermitage@develop` a única retenção é a da fila de saída, de 7 dias; `EnsureAuditPartitionsService` só cria partições (`MONTHS_AHEAD = 2`, linha 14), nenhum job apaga as antigas e a busca só usa `dateFrom` e `dateTo`. O único outro prazo é `ListAuditActionsService.LOOKBACK` de 90 dias, que só limita a lista de ações do filtro. Escrever 13 meses seria prometer um prazo que o código não aplica, e escrever "sem prazo" seria prometer o oposto sem decisão de produto. A página diz só o que o código garante, que os registros não podem ser alterados. Produto decide o prazo, e uma atualização das três páginas o inclui.

**D7. Textos do painel em português, inglês e espanhol saem do i18n do `lancaster`.** Os nomes de botões e campos nas páginas devem bater com `pt-br.json`, `en-us.json` e `es.json` do painel. Quando o nome difere entre idiomas, a página usa o nome do idioma dela.

## Risks / Trade-offs

- **Divergência entre `main` e as branches lidas.** O `frisco` e o `reading` têm commits remotos mais novos que os clones locais. A leitura usou `origin/develop`, `origin/main` e `origin/omnizapi` depois de `git fetch`. Se o `reading` da `develop` não chegar à `main`, a página de IP não afirma nada sobre a rota de compatibilidade, e por isso o risco fica contido em D3.
- **Curinga.** Se a SDK passar a aceitar curinga antes do merge, a página de Domínios fica desatualizada. A implementação deve reconferir `pennsylvania-lester` antes de publicar.
- **Retenção da auditoria.** O painel promete 13 meses e o código não os aplica. A página de Auditoria não cita prazo até a decisão de produto (D8), e o texto do painel segue como está até lá.
- **Páginas com muitas tabelas.** Tabelas em MDX quebram fácil na versão estreita. O `mint dev` precisa conferir a tabela de papéis no celular.
