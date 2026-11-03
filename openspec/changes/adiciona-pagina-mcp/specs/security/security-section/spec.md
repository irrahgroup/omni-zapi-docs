# Spec Delta

## MODIFIED Requirements

### Requirement: Seção Segurança no menu de guias

O menu da aba de guias SHALL ter o grupo **Segurança** (`Security` em inglês, `Seguridad` em espanhol) com sete páginas, nesta ordem: Introdução, Restrição de IP, Domínios da SDK, Autenticação de dois fatores, Time e papéis, Auditoria e Conectar uma IA (MCP). Cada idioma MUST ter o mesmo conjunto de páginas.

Fonte: `docs.json` — grupo `Segurança` da aba Guias pt-BR.

#### Scenario: Menu em português

- **WHEN** o leitor abre a aba **Guias** em português
- **THEN** existe o grupo **Segurança** com as sete páginas na ordem definida

#### Scenario: Paridade entre idiomas

- **WHEN** o leitor troca para inglês ou espanhol
- **THEN** o grupo traz as mesmas sete páginas, com título e descrição traduzidos
- **AND** `python3 scripts/check-docs.py` termina com `check-docs: tudo certo`
