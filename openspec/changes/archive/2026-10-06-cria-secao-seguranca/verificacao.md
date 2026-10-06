# Verificação — cria-secao-seguranca

Implementação de documentação (páginas `.mdx` + `docs.json`). A evidência de cada
requisito é o arquivo da página e a linha. As páginas `en/` e `es/` espelham a
`pt`; as linhas citadas são da versão em português.

Checagens automáticas executadas (manualmente, o repositório não tem CI):
- `python3 scripts/check-docs.py` → `check-docs: tudo certo`.
- `python3 -c "import json;json.load(open('docs.json'))"` → ok.
- `mint broken-links` → sem links quebrados.
- `grep -c 'not allowed'` em cada `ip-restriction.mdx` → 2.
- `grep -nE '13 (meses|months)'` em `audit.mdx` → vazio.

## security-section

- **Seção Segurança no menu de guias** — `docs.json:115` (Segurança), `docs.json:395` (Security), `docs.json:675` (Seguridad); grupo com as seis páginas nos três idiomas.
- **Introdução explica local e benefício** — `security/introduction.mdx:8` (local e acesso só do Owner); `security/introduction.mdx:16`–`:21` (tabela de recursos com onde fica cada um); seção "Por que usar cada uma" com o benefício de cada recurso.

## ip-restriction

- **Regras de funcionamento** — `security/ip-restriction.mdx:14` (comparação exata, sem CIDR), `:15` (vale para todas as chamadas com Secret Key).
- **Prazo de propagação** — `security/ip-restriction.mdx:17` (até 10 minutos).
- **Resposta de bloqueio** — `security/ip-restriction.mdx:47` (`{"error": "203.0.113.10 not allowed"}`), `:51` (`"ip not allowed"`).
- **Passo a passo e quem pode alterar** — `security/ip-restriction.mdx:21`–`:25` (passos, IP, descrição, código de confirmação), `:27` (só o Owner altera).

## sdk-authorized-domains

- **Cadastro por origem exata** — `security/sdk-domains.mdx:23` (origem exata com `https://`, sem curinga).
- **Painel do Omni sempre liberado** — `security/sdk-domains.mdx` (regra "o painel sempre pode abrir o SDK").
- **Quem configura** — `security/sdk-domains.mdx` (passo a passo em Administração → Segurança) e `security/introduction.mdx:8` (só o Owner acessa o menu).

## two-factor-authentication

- **Escopo do 2FA** — `security/two-factor.mdx:29` (protege o login no painel; a API segue pela Secret Key).
- **Ativação e desativação** — `security/two-factor.mdx` (seção "Ativar") e `:23`–`:25` (seção "Desativar").

## team-roles

- **Permissões de cada papel** — `security/team.mdx:16` (Owner), `:27` (Manager), `:35` (Membro) e tabela em `:44`–`:51`.
- **Convite e aceite** — `security/team.mdx:85` (convidar), `:92` e `:108` (quem aceita entra como Membro).
- **Promoção e rebaixamento** — `security/team.mdx:63`–`:74` (promover/rebaixar, com prints), `:80` (Owner sem botões).

## audit-log

- **Acesso ao log** — `security/audit.mdx:10` (Administração → Auditoria, Owner e Manager).
- **Conteúdo do registro** — `security/audit.mdx:23` (resultado `SUCCESS`/`FAILURE`/`DENIED` com código HTTP) e campos acima.
- **Filtros e escopo de visualização** — `security/audit.mdx` (seção de filtros e escopo).
- **Exportação CSV** — `security/audit.mdx:42` (CSV da página atual, com os filtros).
- **Retenção só depois de confirmada** — `security/audit.mdx:25` (registros imutáveis; sem citar prazo de retenção, por não estar confirmado no código).

## navigation/guides-menu

- **Grupo Canais aberto e sem botão de recolher** — `docs.json:127` (grupo Canais com `expanded: true`, sem `root`/`directory`, Introdução primeiro) nos três idiomas.
- **Ícone do site no rodapé** — `docs.json:960` (`footer.socials.website` = `https://omni.z-api.io`).

## Observação
Implementado e verificado na mesma sessão. Recomenda-se uma conferência visual final no `mint dev` (tarefa 5.7) por outra pessoa antes do merge.
