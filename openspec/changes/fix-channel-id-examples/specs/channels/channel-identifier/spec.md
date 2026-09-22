# Spec Delta

## Purpose

Define o formato do identificador de canal na documentação do Omni Z-API: o que a criação de canal devolve, e como esse mesmo valor deve aparecer nas chamadas seguintes que o consomem.

## ADDED Requirements

### Requirement: Formato do identificador de canal

Todo exemplo de identificador de canal na documentação SHALL usar o formato real devolvido pela API: uma string hexadecimal de 32 caracteres maiúsculos, sem separadores.

A documentação MUST NOT apresentar o identificador de canal no formato UUID com hífens, que a API não devolve.

Fonte: `pt/channels/openapi-create.json:49` — exemplo da resposta de `createChannel`; `webhooks/payloads.mdx:63` — `channel_id` no payload de webhook, já no formato hexadecimal.

#### Scenario: Resposta da criação de canal

- **WHEN** um leitor consulta a resposta de sucesso da página Criar canal, em qualquer idioma
- **THEN** o exemplo exibido é `{ "id": "019E4C54B1B375A28970B605CA9B03C3" }`
- **AND** nenhum exemplo de identificador de canal usa o formato UUID com hífens

#### Scenario: Parâmetro de caminho que recebe o identificador

- **WHEN** um endpoint declara `channelId` como parâmetro e o descreve como obtido na criação do canal
- **THEN** o exemplo desse parâmetro usa o mesmo formato hexadecimal de 32 caracteres

### Requirement: O identificador é o mesmo ao longo do percurso

O valor de exemplo do identificador de canal SHALL ser idêntico nas páginas que compõem o percurso do integrador — criar o canal e depois conectá-lo —, de modo que o leitor reconheça que se trata do mesmo canal e não de identificadores distintos.

Fonte: `pt/channels/openapi-create.json:49` — onde o identificador é produzido; `pt/channels/openapi-connect.json:22` — onde é consumido, com a descrição "ID do canal (obtido via Criar canal)".

#### Scenario: Percurso criar e conectar

- **WHEN** um leitor vai da página Criar canal para a página Conectar canal
- **THEN** encontra o mesmo valor de identificador nos dois exemplos

#### Scenario: Paridade entre idiomas

- **WHEN** o mesmo exemplo é consultado em português, inglês e espanhol
- **THEN** os três exibem o mesmo valor de identificador

### Requirement: Identificadores de outros sistemas não são afetados

A padronização SHALL se aplicar apenas ao identificador de canal. Valores em formato UUID que pertencem a outros sistemas MUST permanecer inalterados.

Fonte: `pt/messages/openapi-sticker.json:35` — UUIDs que compõem a URL de um pacote de figurinhas em CDN externo.

#### Scenario: URL de pacote de figurinhas

- **WHEN** um leitor consulta o exemplo de envio de sticker
- **THEN** a URL do CDN mantém os UUIDs originais, sem substituição
