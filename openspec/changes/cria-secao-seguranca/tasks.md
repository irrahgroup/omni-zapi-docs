# Tasks

## 1. Linha de base

- [ ] 1.1 Registrar o estado do menu: `python3 -c "import json;d=json.load(open('docs.json'));[print(l['language'],[ (g['group'],g.get('expanded'),g['pages'][:3]) for t in l['tabs'] for g in t['groups'] if g['group'] in ('Canais','Channels','Canales')]) for l in d['navigation']['languages']]"`
- [ ] 1.2 Rodar `python3 scripts/check-docs.py` antes de mexer e anotar o resultado: executado manualmente por quem implementa, porque o repositório não tem `.github/workflows/`

## 2. Escrever as páginas em português

- [ ] 2.1 `security/introduction.mdx`, com os cinco recursos, a localização no painel, o benefício e os links (spec `security-section`)
- [ ] 2.2 `security/ip-restriction.mdx`: passo a passo, regras, 10 minutos, `400` com os dois corpos e quem altera (spec `ip-restriction`)
- [ ] 2.3 `security/sdk-domains.mdx`: origem exata, sem curinga, painel do Omni sempre liberado, quem configura (spec `sdk-authorized-domains`)
- [ ] 2.4 `security/two-factor.mdx`: escopo, ativação, login e desativação (spec `two-factor-authentication`)
- [ ] 2.5 `security/team.mdx`: tabela de permissões, convite, aceite como Membro e troca de papel (spec `team-roles`)
- [ ] 2.6 `security/audit.mdx`: acesso, registro, filtros, escopo e CSV, sem prazo de retenção (spec `audit-log`)

## 3. Traduzir

- [ ] 3.1 Criar as seis páginas em `en/security/` com o mesmo conteúdo e os nomes de tela do `en-us.json` do painel
- [ ] 3.2 Criar as seis páginas em `es/security/` com o mesmo conteúdo e os nomes de tela do `es.json` do painel
- [ ] 3.3 Conferir que o `frontmatter` (`title`, `description`) existe e está traduzido nas 18 páginas

## 4. Menu e rodapé

- [ ] 4.1 No `docs.json`, inserir o grupo **Segurança** / **Security** / **Seguridad** (ícone `shield-halved`, `expanded: true`) na aba de guias dos três idiomas, depois de **Conceitos do WhatsApp**
- [ ] 4.2 No grupo Canais da aba de guias dos três idiomas, pôr `expanded: true`, **remover `root` e `directory`** e deixar as páginas na ordem `channels/introduction`, `channels/overview`, `channels/message-support` (com o prefixo do idioma em `en/` e `es/`)
- [ ] 4.3 Trocar `footer.socials.website` para `https://omni.z-api.io`; não mexer em `snippets/variables.mdx`

## 5. Verificar

- [ ] 5.1 `python3 scripts/check-docs.py` termina com `check-docs: tudo certo`: executado manualmente por quem implementa, sem execução automática em PR, push ou merge
- [ ] 5.2 `python3 -c "import json;json.load(open('docs.json'));print('ok')"`
- [ ] 5.3 Confirmar que nenhuma página sugere curinga: `grep -rn '\*\.' {,en/,es/}security/sdk-domains.mdx` não pode mostrar `*.` como exemplo válido de cadastro
- [ ] 5.4 Confirmar o corpo de bloqueio nas três páginas de IP: `grep -c 'not allowed' {,en/,es/}security/ip-restriction.mdx` retorna 2 ou mais em cada uma
- [ ] 5.5 Confirmar o prazo de IP e a ausência de retenção: `grep -n '10 min' {,en/,es/}security/ip-restriction.mdx` deve achar a linha nas três; `grep -nE '13 (meses|months)' {,en/,es/}security/audit.mdx` deve retornar vazio, e a página deve dizer que os registros não podem ser alterados
- [ ] 5.6 Confirmar o diff: `git diff --stat` e `git status --short` mostram as 18 páginas novas e `docs.json`, e nenhum outro arquivo fora de `openspec/`
- [ ] 5.7 Subir `mint dev`, abrir as seis páginas nos três idiomas, conferir o menu (Segurança aberta, Canais aberto com Introdução primeiro), a tabela de papéis em tela estreita e o link do rodapé; encerrar o servidor
- [ ] 5.8 Rodar `mint broken-links` e corrigir os links das páginas novas
- [ ] 5.9 Confirmar o grupo Canais no `docs.json`: `python3 -c "import json;d=json.load(open('docs.json'));[print(l['language'],[{k:v for k,v in g.items() if k!='pages'} for t in l['tabs'] for g in t['groups'] if g['group'] in ('Canais','Channels','Canales') and t['tab'] in ('Guias','Guides','Guías')]) for l in d['navigation']['languages']]"` mostra `expanded: True` e nenhum `root` nem `directory`

## 6. Pendências para fora desta change

- [ ] 6.1 Abrir tarefa para o time do painel e da SDK sobre o curinga (Questão em aberto da proposta)
- [ ] 6.3 Levar a produto (com quem mantém a auditoria no `pennsylvania-hermitage`) que os 13 meses do painel não são aplicados no código (só há criação de partições, sem remoção, e a busca não limita o período); com a decisão, atualizar `security/audit.mdx` nos três idiomas e a spec `audit-log`
- [ ] 6.2 Avisar quem mantém a `pennsylvania-reading` que a rota de compatibilidade da `main` ainda difere da `develop` quanto à regra de IP (D3)
