# Tasks

## 1. Páginas

- [x] 1.1 Trocar o aviso de `{,en/,es/}messages/send-location.mdx` pelo aviso da limitação do WhatsApp Web, mantendo o rótulo de estado de cada idioma
- [x] 1.2 Acrescentar à conceituação das três páginas o formato das coordenadas: texto, como no exemplo, sem dizer que número é aceito (5.3)
- [x] 1.3 Verificar com `grep -rn "unmarshal\|não há caminho\|no working path\|no hay camino" messages en/messages es/messages` que nada sobrou

## 2. Notas por canal

- [x] 2.1 Em `snippets/channel-support.mdx`, trocar a nota única de `LOCATION` por notas de WhatsApp Web, Instagram, Messenger e Telegram, nos três idiomas
- [x] 2.2 Verificar com `git diff snippets/channel-support.mdx` que a linha `LOCATION` da `MATRIX` não mudou

## 3. OpenAPI

- [x] 3.1 Acrescentar à descrição de `latitude` e `longitude` dos três `openapi-location.json` que o valor vai em texto, como no exemplo, sem dizer que número é aceito (5.3) e sem mudar `type` nem `example`
- [x] 3.2 Validar os três JSON com `python3 -m json.tool`

## 4. Verificação

- [x] 4.1 Buscar `reading`, `frisco`, `barling`, `fouke`, `Go struct` e `Jackson` nos arquivos alterados fora de `openspec/`: vazio
- [x] 4.2 Rodar `python3 scripts/check-docs.py` e confirmar `check-docs: tudo certo`. Executado à mão por quem implementa: o repositório não tem `.github/workflows/`, então não há execução automática em PR
- [x] 4.3 Rodar `mint broken-links` e confirmar que nenhum link novo quebrou. Executado à mão por quem implementa
- [x] 4.4 Subir `mint dev` e conferir no HTML servido das três páginas o aviso novo, o parágrafo das coordenadas e as quatro notas; encerrar o servidor

## 5. Correções da revisão de produto (14/10/2026)

- [x] 5.1 Trocar, nos três idiomas e no snippet, o texto que dizia que as coordenadas e o endereço vão no WhatsApp Web por "o nome do lugar não é repassado", sem prometer entrega. Verificar com `grep -rn "vão normalmente\|go as usual\|van con normalidad\|As coordenadas e o endereço vão\|The coordinates and the address go\|Las coordenadas y la dirección van" messages en/messages es/messages snippets`: vazio
- [x] 5.2 Trocar a nota do Instagram, nos três idiomas, por "não é entregue, mesmo quando a chamada é aceita"
- [x] 5.3 Tirar "número também é aceito" das três páginas e dos três OpenAPI. Verificar com `grep -rn "Número também\|number is accepted\|número también" messages en/messages es/messages pt/messages`: vazio
- [x] 5.4 Citar o `irrahgroup/pennsylvania-reading#22` e a tarefa 3.4 dele na proposta
- [x] 5.5 Rodar de novo `python3 scripts/check-docs.py`, os três `python3 -m json.tool` e `mint broken-links`, à mão, por quem corrige
- [ ] 5.6 **Antes do merge**, a tarefa 3.2 do `irrahgroup/arkansas-barling#200` registra o que a Z-API faz com `title` nulo. Se a localização não for entregue, este PR segue o ramo "Se a 3.2 mostrar que `title` nulo não é entregue" da proposta antes do merge: o requisito, o aviso, a nota, a célula da matriz e o PR do lancaster. Se for entregue com coordenadas e endereço, o texto pode dizê-lo, em PR próprio. Em 14/10/2026 a 3.2 ainda não rodou: ela exige um envio real em staging, ainda não autorizado. Quem confere: o revisor deste PR, pelo comentário da 3.2 aqui. O merge é do dono
