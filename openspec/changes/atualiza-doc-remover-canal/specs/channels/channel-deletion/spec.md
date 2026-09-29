# Spec Delta

## Purpose

Define o que a documentação de Remover canal do Omni Z-API afirma ao parceiro sobre a exclusão: o efeito dela, as condições para ela acontecer e o erro `502` devolvido quando o serviço interno falha.

## ADDED Requirements

### Requirement: A exclusão é descrita pelo efeito para o parceiro

A página Remover canal SHALL descrever a exclusão pelo que o parceiro observa: o canal deixa de poder ser usado e a exclusão não pode ser desfeita pela API.

A documentação MUST NOT afirmar que o canal é removido fisicamente do sistema, e MUST NOT descrever como o sistema guarda o canal excluído — em especial, exclusão lógica, marcação interna ou preservação de registros.

Fonte: `channels/delete-channel.mdx:11` — conceituação; `pt/channels/openapi-delete.json:13` — descrição do endpoint.

#### Scenario: Conceituação da página

- **WHEN** um leitor abre a página Remover canal, em qualquer idioma
- **THEN** a conceituação diz que o canal excluído não pode mais ser usado e que a exclusão não se desfaz pela API
- **AND** o texto não contém "fisicamente", "permanentemente" nem menção a exclusão lógica

#### Scenario: Descrição do endpoint

- **WHEN** um leitor consulta a descrição de `DELETE /v1/channels/{channelId}` no OpenAPI, em qualquer idioma
- **THEN** a descrição não afirma remoção física nem descreve o armazenamento interno

### Requirement: Condição de canal desconectado

A página SHALL informar que o canal precisa estar desconectado para ser excluído e citar o `422` com `INSTANCE_STILL_CONNECTED`, com link para Desconectar canal.

Fonte: `channels/delete-channel.mdx:19` — condição de desconexão; `pt/channels/openapi-delete.json:80` — exemplo `INSTANCE_STILL_CONNECTED` já documentado no OpenAPI.

#### Scenario: Canal ainda conectado

- **WHEN** um leitor consulta as condições para exclusão
- **THEN** encontra que o canal deve estar desconectado, com o código `INSTANCE_STILL_CONNECTED` e o link para Desconectar canal

#### Scenario: Paridade entre idiomas

- **WHEN** a mesma página é consultada em português, inglês e espanhol
- **THEN** as três trazem a mesma condição de canal desconectado, com o código `INSTANCE_STILL_CONNECTED`
- **AND** as três mostram o mesmo corpo do `502`, `{ "error": "Hermitage deleteChannel failed" }`

### Requirement: Corpo do erro 502

A documentação SHALL apresentar o corpo real do `502` de `DELETE /v1/channels/{channelId}`: `{"error": "Hermitage deleteChannel failed"}`, com `error` como texto e sem campo `message`.

O exemplo do `502` no OpenAPI MUST NOT usar o formato `{"error": <número>, "message": <texto>}`, e a página SHALL orientar o parceiro a tentar de novo e acionar o suporte se o erro persistir.

Fonte: `pt/channels/openapi-delete.json:95` — exemplo do `502`; frisco #55, `HermitageHttpClientProvider.assertSuccess`, que devolve `502 {"error":"Hermitage <operação> failed"}` sem o corpo interno.

#### Scenario: Exemplo do 502 no OpenAPI

- **WHEN** um leitor consulta a resposta `502` no OpenAPI, em qualquer idioma
- **THEN** o exemplo é `{ "error": "Hermitage deleteChannel failed" }`
- **AND** o schema declara `error` como string, sem `message`

#### Scenario: Seção de erro na página

- **WHEN** um leitor procura o que fazer diante do `502`
- **THEN** a página mostra o mesmo corpo e diz para tentar novamente e, persistindo, falar com o suporte
- **AND** a página não mostra timestamp, path nem status interno
