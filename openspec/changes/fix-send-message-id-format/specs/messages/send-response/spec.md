# Spec Delta

## Purpose

Define o que a documentação deve afirmar sobre a resposta `200` dos endpoints de envio da API unificada do Omni Z-API: o formato do `messageId` devolvido, a paridade desse conteúdo entre português, inglês e espanhol, e a correlação desse identificador com o `message._id` recebido no webhook.

## ADDED Requirements

### Requirement: Formato do messageId nas respostas de envio

Toda resposta `200` documentada para os endpoints de envio da API unificada (`POST /v1/channels/{channelId}/messages`) SHALL apresentar o `messageId` no formato real devolvido pela API: uma string hexadecimal de 32 caracteres maiúsculos, sem prefixo.

A documentação MUST NOT usar o formato `wamid.*` da Meta como exemplo de resposta de envio, por ser o identificador de um sistema externo e não o que o Omni Z-API retorna.

#### Scenario: Exemplo do 200 em um endpoint de envio

- **WHEN** um leitor consulta a resposta `200` de qualquer endpoint de envio da API unificada (TEXT, IMAGE, AUDIO, VIDEO, CONTACT, STICKER, LOCATION, INTERACTIVE_ACTION, INTERACTIVE_BUTTON ou TEMPLATE)
- **THEN** o exemplo exibido é `{ "messageId": "01A0C92D0C957FE98B73C8BA0CACF741" }`
- **AND** nenhum exemplo de resposta de envio contém a string `wamid.`

#### Scenario: Descrição do campo declara o formato

- **WHEN** um leitor inspeciona o schema da resposta de envio
- **THEN** a descrição do campo `messageId` informa que o valor é um identificador hexadecimal de 32 caracteres maiúsculos
- **AND** essa descrição aparece no idioma da página consultada

#### Scenario: Endpoint com resposta declarada inline

- **WHEN** um endpoint de envio declara o `200` diretamente na operação, em vez de referenciar uma resposta compartilhada
- **THEN** esse exemplo inline também usa o formato hexadecimal de 32 caracteres

### Requirement: Correlação entre o envio e o evento de webhook

A documentação SHALL informar que o `messageId` devolvido na resposta `200` do envio é o mesmo valor entregue no webhook como `message._id`, permitindo que o integrador reconcilie a chamada de envio com o evento recebido.

#### Scenario: Leitor busca como correlacionar envio e webhook

- **WHEN** um leitor consulta a página de introdução de mensagens
- **THEN** encontra a informação de que o `messageId` da resposta de envio corresponde ao `message._id` do payload de webhook
- **AND** a informação está disponível em português, inglês e espanhol

### Requirement: Paridade entre idiomas

O formato do `messageId`, o valor de exemplo e a nota de correlação com o webhook SHALL ser idênticos em conteúdo nas versões em português, inglês e espanhol; apenas o texto descritivo varia conforme o idioma.

#### Scenario: Comparação entre os três idiomas

- **WHEN** a mesma resposta de envio é consultada em `pt`, `en` e `es`
- **THEN** os três exibem o mesmo valor de exemplo para `messageId`
- **AND** os três declaram o mesmo formato para o campo

### Requirement: Preservação dos contratos fora do escopo de envio

A correção do formato SHALL se aplicar apenas às respostas de envio da API unificada. Os demais contratos documentados MUST permanecer inalterados.

#### Scenario: Camada de compatibilidade Z-API

- **WHEN** um leitor consulta a resposta de um endpoint de compatibilidade Z-API
- **THEN** continua vendo o contrato legado com `zaapId` e o `messageId` no formato próprio da Z-API
- **AND** nenhum valor dessa seção é substituído pelo formato da API unificada

#### Scenario: Payloads de webhook

- **WHEN** um leitor consulta a estrutura dos payloads de webhook
- **THEN** o identificador da mensagem continua sendo apresentado como `message._id` no formato hexadecimal já documentado, sem alteração
