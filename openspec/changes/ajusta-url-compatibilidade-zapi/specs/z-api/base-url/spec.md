# Spec Delta

## Purpose

Define qual host a documentação apresenta para a camada de compatibilidade Z-API, e como ele se distingue do host da API unificada e do host da Z-API original, que convivem nas mesmas páginas.

## ADDED Requirements

### Requirement: Host da camada de compatibilidade

Todo endereço da camada de compatibilidade Z-API apresentado na documentação SHALL usar `https://zapi.omni.z-api.io`. A documentação MUST NOT apresentar `https://api.omni.z-api.io` como host da compatibilidade.

Fonte: `pt/z-api/openapi.json:10` — `servers[0].url`; `z-api/authentication.mdx:51` — exemplo `curl`; `z-api/introduction.mdx:22` — tabela de comparação.

#### Scenario: Servidor declarado no spec da compatibilidade

- **WHEN** um leitor consulta qualquer endpoint da seção de compatibilidade Z-API
- **THEN** o servidor exibido é `https://zapi.omni.z-api.io/channels/{channel_id}/token/{channel_token}`
- **AND** isso vale nos três idiomas

#### Scenario: Exemplos executáveis

- **WHEN** um leitor copia um exemplo `curl` das páginas de autenticação ou introdução da compatibilidade
- **THEN** o comando aponta para `zapi.omni.z-api.io`

### Requirement: Os três hosts permanecem distinguíveis

As páginas de compatibilidade citam três hosts com papéis diferentes, e a mudança SHALL preservar essa distinção.

| Host | Papel |
|---|---|
| `api.z-api.io` | Z-API original, de onde o cliente migra |
| `zapi.omni.z-api.io` | Camada de compatibilidade, para onde ele vai |
| `api.omni.z-api.io` | API unificada, superfície nova e independente |

Fonte: `z-api/introduction.mdx:22` — tabela que contrapõe origem e destino; `z-api/introduction.mdx:86` — texto de migração.

#### Scenario: Tabela de comparação

- **WHEN** um leitor consulta a tabela que contrapõe Z-API e Omni na página de introdução
- **THEN** a coluna de origem continua mostrando `https://api.z-api.io`
- **AND** a coluna de destino mostra `https://zapi.omni.z-api.io`

#### Scenario: Instrução de migração

- **WHEN** um leitor lê o texto que diz o que substituir ao migrar
- **THEN** ele indica trocar `https://api.z-api.io` por `https://zapi.omni.z-api.io`

#### Scenario: A API unificada não é afetada

- **WHEN** um leitor consulta qualquer endpoint fora da seção de compatibilidade
- **THEN** o servidor continua sendo `https://api.omni.z-api.io`
