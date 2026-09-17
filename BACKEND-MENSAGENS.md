# Backend — localização, contato e lista de opções

Três tipos de mensagem que a API oficial da Meta suporta e que o Omni Z-API ainda não entrega.
Cada um tem três frentes: **envio nativo**, **compatibilidade Z-API** e **recebimento por webhook**.

As páginas de documentação já existem com aviso de *em desenvolvimento*. Assim que cada frente subir,
o aviso sai e a página é publicada como funcional.

---

## 1. Localização — `content.type: LOCATION`

**Estado:** quebrado nos dois caminhos possíveis. Não existe forma de fazer funcionar hoje.

| Entrada | Hoje |
|---|---|
| `"latitude": "-23.0696347"` (string) | `400` — `json: cannot unmarshal string into Go struct field SendMessageInput.latitude of type float64` |
| `"latitude": -23.0696347` (number) | `200`, mas a mensagem **não chega** ao destinatário |

### 1.1 Aceitar string e número

O struct hoje declara `float64` estrito. A [Meta documenta as coordenadas como string](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-messages)
(`"37.44216251868683"`), e a Z-API também manda string — então quem copia o corpo da Z-API toma erro no
primeiro teste. **O exemplo publicado na nossa própria documentação manda string**, ou seja, o payload que
a gente ensina é o que falha.

Solução: `UnmarshalJSON` customizado no campo, aceitando os dois e normalizando para `float64` por dentro.

```go
type Coord float64

func (c *Coord) UnmarshalJSON(b []byte) error {
    s := strings.Trim(string(b), `"`)
    v, err := strconv.ParseFloat(s, 64)
    if err != nil {
        return fmt.Errorf("latitude/longitude inválida: %q", s)
    }
    *c = Coord(v)
    return nil
}
```

### 1.2 Descobrir por que o número não entrega

Com número não há erro de parse, então o problema está depois: mapeamento para o payload da Meta,
ou os campos não sendo repassados. Investigar com log do corpo enviado à Cloud API.

### 1.3 Payload que a Meta espera

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "location",
  "location": {
    "latitude": "-23.0696347",
    "longitude": "-50.4357913",
    "name": "Google Brasil",
    "address": "Av. Brg. Faria Lima, 3477 - Itaim Bibi, São Paulo - SP"
  }
}
```

`name` e `address` são opcionais, mas o WhatsApp só mostra o nome do lugar no balão quando os dois vão juntos.

### 1.4 Compatibilidade Z-API

A aba de compatibilidade **não tem página de `send-location`**. Conferir se a rota existe. Se existir,
ela precisa aceitar o corpo da Z-API verbatim; se não existir, precisa ser criada — a promessa da camada
é que só mudam a base URL e o header.

### 1.5 Recebimento

Quando o cliente manda um ponto, a Meta entrega `messages[].location` com os mesmos campos.
**Hoje isso não vira nada no nosso webhook**: os tipos de conteúdo documentados são `TEXT`, `IMAGE`,
`AUDIO`, `VIDEO`, `STICKER`, `CONTACT_ARRAY`, `INTERACTIVE_BUTTON` e `INTERACTIVE_ACTION` — não há
localização na entrada, embora exista na saída.

Precisa de um conteúdo `LOCATION` em `contents[]`, simétrico ao que a gente envia.

### Critérios de aceite

- [ ] `latitude`/`longitude` aceitos como string e como número, na rota nativa e na de compatibilidade
- [ ] coordenada inválida devolve `400` com mensagem legível, não erro de unmarshal
- [ ] mensagem chega ao destinatário com o pin no lugar certo
- [ ] `name` e `address` aparecem no balão quando enviados
- [ ] localização recebida do cliente chega no webhook como conteúdo `LOCATION`

---

## 2. Contato — `content.type: CONTACT`

**Estado:** funciona para um contato. Do segundo item de `attachments` em diante, nada é enviado.

### 2.1 Enviar a lista inteira

A [Meta aceita até 257 contatos](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contacts-messages)
por mensagem. O nosso `attachments` já é lista no contrato — é iterar em vez de pegar o primeiro.

### 2.2 Ampliar o contato

O schema atual leva só `name` (string) e `phones` (array de string). O contato da Meta é bem mais rico,
e o único campo obrigatório é `name.formatted_name`:

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "Gutemberg Fernandes",
        "first_name": "Gutemberg",
        "last_name": "Fernandes"
      },
      "phones": [
        { "phone": "+5511888888888", "type": "CELL", "wa_id": "5511888888888" }
      ],
      "emails": [{ "email": "gutemberg@empresa.com", "type": "WORK" }],
      "addresses": [
        {
          "street": "Av. Paulista, 1000",
          "city": "São Paulo",
          "state": "SP",
          "zip": "01310-100",
          "country": "Brasil",
          "country_code": "BR",
          "type": "WORK"
        }
      ],
      "org": { "company": "Empresa LTDA", "department": "Suporte", "title": "Analista" },
      "urls": [{ "url": "https://empresa.com", "type": "WORK" }],
      "birthday": "1990-05-20"
    }
  ]
}
```

Duas diferenças de forma em relação ao nosso contrato: na Meta, `name` é **objeto** e `phones` é lista de
**objeto**, não de string. Sugestão: manter o nosso contrato simples e converter por dentro, mas expondo
pelo menos `emails` e `org`, que são os mais pedidos.

O `wa_id` é o que faz o WhatsApp oferecer o botão de conversar com o contato. Sem ele o cartão chega, mas
sem ação.

### 2.3 Compatibilidade Z-API

Temos `/send-contact` no singular. O `/send-contacts` da Z-API, no plural, **não existe** do nosso lado.

### 2.4 Recebimento

Este já funciona, e com uma ironia: o webhook entrega `CONTACT_ARRAY` com `contacts[]` **múltiplos**
(`first_name`, `last_name`, `name`, `phones`). Ou seja, **a gente já recebe vários contatos e só consegue
enviar um**. A assimetria é só na saída.

Vale alinhar a nomenclatura: na saída o tipo é `CONTACT`, na entrada é `CONTACT_ARRAY`.

### Critérios de aceite

- [ ] `attachments` com N contatos envia os N, respeitando o teto de 257
- [ ] `emails`, `addresses`, `org`, `urls` e `birthday` aceitos e repassados
- [ ] `wa_id` preenchido quando o telefone é um número de WhatsApp
- [ ] `/send-contacts` respondendo na camada de compatibilidade
- [ ] acima de 257 contatos, `400` com mensagem legível

---

## 3. Lista de opções — `content.type: INTERACTIVE_LIST`

**Estado:** não existe. Nem rota nativa, nem rota de compatibilidade. O que existe é `send-button-list`,
que é outra coisa: botões de resposta com mídia.

### 3.1 Payload que a Meta espera

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": { "type": "text", "text": "Cardápio" },
    "body": { "text": "Escolha uma opção" },
    "footer": { "text": "Entrega em 40 min" },
    "action": {
      "button": "Ver opções",
      "sections": [
        {
          "title": "Pizzas",
          "rows": [
            {
              "id": "pizza_marg",
              "title": "Margherita",
              "description": "Molho, muçarela e manjericão"
            }
          ]
        }
      ]
    }
  }
}
```

### 3.2 Limites que precisam ser validados

Fonte: [interactive list messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-list-messages).

| Regra | Limite |
|---|---|
| Seções | até 10 |
| Linhas | até **10 somando todas as seções** |
| Texto do botão | 20 caracteres |
| Título da linha | 24 caracteres |
| Descrição da linha | 72 caracteres |
| `id` da linha | único dentro da mensagem |

O limite de **10 linhas no total** é o que mais vai pegar quem vem da Z-API, porque é natural supor 10 por
seção. Vale recusar com `400` e mensagem explícita em vez de deixar a Meta recusar.

### 3.3 Compatibilidade Z-API

`/send-option-list` precisa nascer, traduzindo o corpo da Z-API para o formato acima.

### 3.4 Recebimento

É a metade que dá sentido à lista. Quando o cliente escolhe uma linha, a Meta entrega:

```json
"interactive": {
  "type": "list_reply",
  "list_reply": {
    "id": "priority_express",
    "title": "Priority Mail Express",
    "description": "Next Day to 2 Days"
  }
}
```

O `id` é o mesmo que foi enviado na linha, e é por ele que a aplicação do cliente identifica a escolha.
Precisa de um conteúdo próprio no nosso webhook.

O irmão dele, `button_reply`, tem a mesma forma com `id` e `title`, e também não aparece na nossa
documentação de payloads — vale fechar os dois juntos.

### Critérios de aceite

- [ ] `INTERACTIVE_LIST` enviando com seções, linhas, header e footer
- [ ] validação dos seis limites acima, com `400` legível
- [ ] `/send-option-list` respondendo na camada de compatibilidade
- [ ] escolha do cliente chegando no webhook com `id`, `title` e `description`
- [ ] `button_reply` chegando no webhook com `id` e `title`

---

## Transversal: o webhook só documenta o que sai

Todos os exemplos de payload de webhook na documentação estão com `metadata.from_me: true` — são ecos de
mensagem enviada. O formato de **mensagem recebida** não está ilustrado em nenhum tipo.

Para estes três isso pesa mais que nos outros, porque localização, contato e lista existem justamente para
o cliente responder. Se o time for mexer nos três agora, é a hora barata de fechar a simetria: cada tipo com
envio, recebimento e eco.

---

## Ordem sugerida

1. **Localização** — é a única com página publicada prometendo algo que não funciona de jeito nenhum, e a
   correção é pequena: o unmarshal e descobrir por que o número não entrega.
2. **Contato** — ampliação, não conserto. O que existe hoje funciona para o caso de um contato.
3. **Lista** — recurso novo. Ninguém está sendo enganado hoje, porque não há página.


---

# Levantamento completo — os demais tipos

A Meta lista **16 tipos** que podem ser enviados dentro da janela de 24 horas, sem template. Sete já funcionam
no Omni Z-API. O quadro abaixo é o que falta, além dos três acima.

| Tipo | Página na doc | Estado |
|---|---|---|
| Documento | `messages/send-document` | não existe nativo; compat Z-API tem bug de `fileName` |
| Reação | `messages/send-reaction` | não existe nativo; compat marcado como não funcional |
| Pedir localização | `messages/send-location-request` | não existe |
| Flow como mensagem | `messages/send-flow` | não existe |
| Catálogo | `messages/send-catalog` | não existe nativo; compat não funcional |
| Produto único | `messages/send-product` | não existe nativo; compat não funcional |
| Multi-produto | `messages/send-product-list` | não existe |
| Detalhes do pedido | `messages/send-order-details` | não existe |
| Status do pedido | `messages/send-order-status` | não existe |

Todas as páginas já estão publicadas com aviso de *em desenvolvimento* e com o corpo proposto para o nosso
contrato. O nome do `content.type` de cada uma está lá e pode ser mudado — se mudar, a doc acompanha.

---

## 4. Documento — `content.type: DOCUMENT`

**Estado:** não existe na API nativa. Não há página de referência, não há spec, e `DOCUMENT` nem aparecia na
tabela de tipos. Na camada de compatibilidade existe, com o bug do `fileName`.

É o tipo mais grave da lista, porque é tão básico quanto imagem — é o único dos quatro tipos de mídia que
ficou de fora.

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "document",
  "document": {
    "link": "https://sualoja.com/nota-fiscal.pdf",
    "caption": "Segue a sua nota fiscal",
    "filename": "nota-fiscal.pdf"
  }
}
```

| Regra | Valor |
|---|---|
| Tamanho | 100 MB |
| Tipos | PDF, Word, Excel, PowerPoint, texto |
| `caption` | 1024 caracteres |
| `filename` | **com extensão** — define o ícone no cliente |

**Bug atual no compat:** `fileName: "documento.pdf"` chega como `documento.pdf.pdf`, e `fileName: "documento"`
chega como `documento.null`. Parece concatenação de extensão sem checar se ela já existe, e sem tratar o caso
vazio.

### Critérios de aceite

- [ ] envio por `link` e por identificador de mídia
- [ ] `filename` com extensão chega exatamente como foi enviado
- [ ] `filename` sem extensão não vira `.null`
- [ ] arquivo acima de 100 MB recusado com `400` legível

---

## 5. Reação — `content.type: REACTION`

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "reaction",
  "reaction": { "message_id": "wamid...", "emoji": "\ud83d\udc4d" }
}
```

Remover é a mesma chamada com `"emoji": ""`.

| Regra | Valor |
|---|---|
| Idade da mensagem alvo | menos de 30 dias |
| Alvo inválido, apagado ou que é reação | erro `131009` |
| Webhooks | só **enviado**; não há entregue nem lido |

### Critérios de aceite

- [ ] aplicar e remover reação
- [ ] `131009` tratado e devolvido com mensagem legível
- [ ] reação recebida do cliente chegando no webhook

---

## 6. Pedir localização — `content.type: LOCATION_REQUEST`

```json
{
  "messaging_product": "whatsapp",
  "type": "interactive",
  "interactive": {
    "type": "location_request_message",
    "body": { "text": "Para calcular o frete, envie sua localização." },
    "action": { "name": "send_location" }
  }
}
```

Texto até 1024 caracteres. O rótulo do botão é fixo da Meta. A resposta chega como mensagem de localização
comum — ou seja, **depende do tipo de recebimento de localização**, que hoje não existe (ver item 1.5).

### Critérios de aceite

- [ ] envio do pedido
- [ ] localização respondida pelo cliente chegando no webhook

---

## 7. Flow como mensagem — `content.type: FLOW`

Hoje temos a seção inteira de Flows — criar, publicar, listar — e o botão de flow em template, mas **não temos
como enviar um flow numa mensagem**, que é o uso mais direto de tudo isso.

```json
{
  "messaging_product": "whatsapp",
  "type": "interactive",
  "interactive": {
    "type": "flow",
    "header": { "type": "text", "text": "Agendamento" },
    "body": { "text": "Escolha o melhor horário." },
    "footer": { "text": "Leva menos de um minuto" },
    "action": {
      "name": "flow",
      "parameters": {
        "flow_message_version": "3",
        "flow_token": "sessao-do-cliente-42",
        "flow_id": "1234567890",
        "flow_cta": "Agendar",
        "flow_action": "navigate",
        "flow_action_payload": { "screen": "AGENDAMENTO", "data": {} }
      }
    }
  }
}
```

| Campo | Regra |
|---|---|
| `flow_message_version` | sempre `"3"` |
| `flow_token` | gerado por nós ou pelo cliente; é o que casa a resposta com a sessão |
| `flow_id` ou `flow_name` | um dos dois |
| `flow_cta` | até 30 caracteres |

Só formulário **publicado** funciona.

### Critérios de aceite

- [ ] envio com `navigate` e com `data_exchange`
- [ ] `flow_token` propagado e devolvido no webhook de resposta
- [ ] flow não publicado recusado com mensagem legível

---

## 8, 9 e 10. Catálogo, produto único e multi-produto

Os três dependem de catálogo conectado no Commerce Manager. São o espelho, dentro da janela, dos modelos de
template que já documentamos.

**Catálogo** — `interactive.type: "catalog_message"`, com `body` obrigatório de até 1024 caracteres, `footer`
opcional de 60 e `parameters.thumbnail_product_retailer_id` opcional.

**Produto único** — `interactive.type: "product"`, com `action.catalog_id` e `action.product_retailer_id`
obrigatórios.

**Multi-produto** — `interactive.type: "product_list"`, com `action.catalog_id` e `action.sections[].product_items[].product_retailer_id`.
Até **30 produtos** somando as seções, e cabeçalho só de texto. Ao menos um SKU precisa existir no catálogo.

### Critérios de aceite

- [ ] os três enviando com catálogo conectado
- [ ] SKU inexistente recusado com mensagem legível
- [ ] acima de 30 produtos recusado antes de chamar a Meta
- [ ] pedido montado pelo cliente chegando no webhook

---

## 11 e 12. Detalhes e status do pedido

**Detalhes do pedido** — `interactive.type: "order_details"` com `action.name: "review_and_pay"`. Leva
`reference_id`, `payment_settings` (Pix dinâmico ou link), `total_amount` com `offset: 100`, `currency: "BRL"`
e `order.items[]` com `retailer_id`, `name`, `amount` e `quantity`.

**Status do pedido** — `interactive.type: "order_status"` com `action.name: "review_order"`. Leva o mesmo
`reference_id`, o novo `order.status` e `payment.status`.

| Regra | Valor |
|---|---|
| Valores | em centavos, `offset: 100` |
| `reference_id` | único por pedido, e é a chave entre os dois |
| Conta | habilitada para pagamentos no Brasil |

### Critérios de aceite

- [ ] fatura enviada e paga com Pix e com link
- [ ] status atualizado referenciando o pedido original
- [ ] resultado do pagamento chegando no webhook

---

## Um fio que atravessa tudo

Nove dos doze itens deste documento dependem de **receber** alguma coisa: a localização que o cliente manda, a
escolha na lista, o pedido montado no catálogo, a resposta do flow, o resultado do pagamento. E o nosso
webhook hoje só documenta oito tipos de conteúdo, todos ilustrados com `from_me: true`.

Fechar o lado do recebimento vale mais que qualquer um dos envios isolados: sem ele, metade desses recursos
manda mensagem e não escuta a resposta.
