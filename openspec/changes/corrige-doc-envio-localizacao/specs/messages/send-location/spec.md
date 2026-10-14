# Spec Delta

## Purpose

Define o que a página de envio de localização diz sobre o funcionamento do endpoint `POST /v1/channels/{channelId}/messages` com `content.type: LOCATION`, o formato das coordenadas e o que chega em cada canal.

## ADDED Requirements

### Requirement: A página não declara o endpoint quebrado

A página de envio de localização MUST NOT afirmar que o endpoint recusa coordenadas em texto, nem que nenhuma localização é entregue. A página MUST NOT citar a mensagem de erro `cannot unmarshal string into Go struct field SendMessageInput.latitude of type float64`. Isso vale nos três idiomas.

Fonte: `messages/send-location.mdx:9` — bloco `<Warning>` de estado; `en/messages/send-location.mdx:9` e `es/messages/send-location.mdx:9` — o mesmo bloco. Fonte complementar: `arkansas-barling` `64d7d9d` — `src/main/java/com/arkansas/barling/core/boundary/input/message/MessageAttachmentInput.java:28` — `MessageAttachmentInput.longitude` e `:29` — `MessageAttachmentInput.latitude`, ambos `String`.

#### Scenario: Leitor abre a página

- **WHEN** um leitor abre a página de envio de localização em qualquer idioma
- **THEN** não encontra a mensagem `cannot unmarshal string`
- **AND** não encontra frase dizendo que não há caminho que funcione no endpoint

### Requirement: A limitação do WhatsApp Web fica registrada

Enquanto o nome do lugar não for repassado no WhatsApp Web, a página SHALL manter o rótulo de estado **Em implementação.** (**Being implemented.**, **En implementación.**) num aviso que fale só dessa limitação: o nome do lugar não é repassado no WhatsApp Web. Enquanto a tarefa 3.2 do `irrahgroup/arkansas-barling#200` não medir o que a Z-API faz com `title` nulo, o aviso e a nota do WhatsApp Web MUST NOT afirmar que as coordenadas ou o endereço chegam.

Fonte: `scripts/check-docs.py:297` — `METHOD_STATUS['LOCATION']`; `scripts/check-docs.py:338` — `check_method_status`. Fonte complementar: `arkansas-fouke` `ed4c9e1` — `fouke-zapi-whatsapp/src/main/java/com/arkansas/fouke/zapi/core/usecase/interactor/message/MessageLocationProcessorInteractor.java:39` — `MessageLocationProcessorInteractor.buildMessageInput`, que manda `title` e não `name`.

#### Scenario: Aviso de estado restrito ao WhatsApp Web

- **WHEN** um leitor lê o aviso de estado da página
- **THEN** o aviso cita o WhatsApp Web e o nome do lugar
- **AND** não cita nenhum outro canal
- **AND** não afirma que as coordenadas ou o endereço chegam no WhatsApp Web

#### Scenario: Linter confere o rótulo

- **WHEN** quem implementa roda `python3 scripts/check-docs.py`
- **THEN** a verificação de estado não acusa as três páginas de localização

### Requirement: Formato das coordenadas

A página SHALL dizer que `latitude` e `longitude` vão em texto, como no exemplo. Enquanto não houver uma chamada de ponta a ponta com número, a página e o OpenAPI MUST NOT dizer que número é aceito. O exemplo do OpenAPI SHALL continuar com as coordenadas em texto.

Fonte: `pt/messages/openapi-location.json:131` — `SendLocationRequest.content.attachments.latitude`; `pt/messages/openapi-location.json:132` — `SendLocationRequest.content.attachments.longitude`. Fonte complementar: `tools.jackson.core:jackson-databind:3.1.5`, a versão de `spring-boot-dependencies-4.1.1.pom:83`, conferida com `JsonMapper` desserializando `-23.0696347` num campo `String`; é indício, sem chamada de ponta a ponta, e por isso a página não promete número.

#### Scenario: Coordenadas na conceituação

- **WHEN** um leitor lê a conceituação da página
- **THEN** encontra que as coordenadas vão em texto, como no exemplo
- **AND** não encontra que número é aceito

#### Scenario: Coordenadas no OpenAPI

- **WHEN** um leitor consulta o schema de `latitude` ou `longitude` no playground
- **THEN** o tipo é `string` e o exemplo é texto
- **AND** a descrição diz em texto, como no exemplo, e não diz que número é aceito

### Requirement: O que chega em cada canal

O quadro de disponibilidade da página de localização SHALL ter uma nota para cada canal que não recebe a localização completa: WhatsApp Web sem o nome do lugar, Instagram sem entrega, mesmo quando a chamada é aceita, Messenger recebendo um texto com o nome, o endereço e um link do mapa, e Telegram só com as coordenadas. A matriz de marcas MUST NOT mudar.

Fonte: `snippets/channel-support.mdx:9` — `MATRIX.LOCATION`; `snippets/channel-support.mdx:44` — `NOTES.LOCATION`. Fonte complementar: `arkansas-fouke` `ed4c9e1` — `fouke-meta-messenger/src/main/java/com/arkansas/fouke/meta/core/usecase/interactor/message/MessageLocationProcessorInteractor.java:46` — `MessageLocationProcessorInteractor.exec`; `fouke-telegram/src/main/java/com/arkansas/fouke/telegram/core/usecase/interactor/message/SendLocationMessageTelegramInteractor.java:40` — `SendLocationMessageTelegramInteractor.exec`; `fouke-meta-instagram/src/main/java/com/arkansas/fouke/meta/core/usecase/interactor/message/MessageUnsupportedTypeProcessorInteractor.java:25` — `MessageUnsupportedTypeProcessorInteractor.UNSUPPORTED_TYPES`.

#### Scenario: Notas por canal

- **WHEN** um leitor vê o quadro de disponibilidade na página de localização
- **THEN** há uma nota de WhatsApp Web, uma de Instagram, uma de Messenger e uma de Telegram
- **AND** a nota do Instagram diz que a mensagem não é entregue, mesmo quando a chamada é aceita
- **AND** a nota do Instagram não promete recusa nem código HTTP

#### Scenario: Matriz intacta

- **WHEN** quem implementa compara `MATRIX.LOCATION` antes e depois
- **THEN** a linha continua `['yes', 'yes', 'no', 'no', 'yes']`

### Requirement: Sem nome de serviço interno

As páginas, as notas e os OpenAPIs desta change MUST NOT citar serviço interno da plataforma.

Fonte: `messages/send-location.mdx:1` — página pública, publicada em `developer.omni.z-api.io`.

#### Scenario: Busca por nome interno

- **WHEN** quem implementa busca `reading`, `frisco`, `barling`, `fouke`, `Go struct` e `Jackson` nos arquivos alterados fora de `openspec/`
- **THEN** a busca não encontra nada
