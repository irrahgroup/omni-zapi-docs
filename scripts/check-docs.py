#!/usr/bin/env python3
"""
Linter de paridade da documentacao Omni Z-API.

Roda na raiz do repo (onde vive o docs.json):
    python3 scripts/check-docs.py

Sai com codigo 1 se achar qualquer problema, para poder plugar no CI.
"""
import glob
import json
import os
import re
import sys

LANGS = {'pt-BR': '', 'en': 'en/', 'es': 'es/'}
SNIPPET_EXPORTS = {}  # preenchido em check_imports
problems = []


def fail(check, msg):
    problems.append((check, msg))


def load_docs():
    with open('docs.json', encoding='utf-8') as fh:
        return json.load(fh)


def nav_pages(node, out):
    if isinstance(node, dict):
        if node.get('root'):
            out.append(node['root'])
        for pg in node.get('pages', []):
            if isinstance(pg, str):
                out.append(pg)
            else:
                nav_pages(pg, out)


def check_json_valid():
    for f in sorted(glob.glob('**/*.json', recursive=True)):
        if 'node_modules' in f:
            continue
        try:
            with open(f, encoding='utf-8') as fh:
                json.load(fh)
        except Exception as exc:
            fail('json', f'{f}: {exc}')


def check_nav(docs):
    for lang in docs['navigation']['languages']:
        out = []
        for tab in lang['tabs']:
            for group in tab['groups']:
                nav_pages(group, out)
        for pg in out:
            if not os.path.exists(pg + '.mdx'):
                fail('nav', f"[{lang['language']}] pagina inexistente: {pg}.mdx")


def check_orphans(docs):
    nav = set()
    for lang in docs['navigation']['languages']:
        for tab in lang['tabs']:
            for group in tab['groups']:
                out = []
                nav_pages(group, out)
                nav |= set(out)
    every = {f[:-4] for f in glob.glob('**/*.mdx', recursive=True)
             if not f.startswith('snippets/')}
    for pg in sorted(every - nav):
        fail('orfa', f'pagina fora da navegacao: {pg}.mdx')


def check_openapi_array(docs):
    for url in docs['openapi']:
        if not os.path.exists('.' + url):
            fail('openapi', f'ref inexistente em docs.json: {url}')


def check_openapi_frontmatter():
    for f in sorted(glob.glob('**/*.mdx', recursive=True)):
        with open(f, encoding='utf-8') as fh:
            s = fh.read()
        m = re.search(r'^openapi:\s*"([^"]+)"', s, re.M)
        if not m:
            continue
        parts = m.group(1).split()
        if not parts[0].endswith('.json'):
            continue  # usa o array global de openapi
        spec, method, path = parts[0], parts[1], parts[2]
        if not os.path.exists('.' + spec):
            fail('openapi', f'{f}: spec inexistente {spec}')
            continue
        with open('.' + spec, encoding='utf-8') as fh:
            j = json.load(fh)
        if path not in j.get('paths', {}):
            fail('openapi', f'{f}: path ausente no spec: {path}')
        elif method.lower() not in j['paths'][path]:
            fail('openapi', f'{f}: metodo ausente: {method} {path}')


def check_links():
    for f in sorted(glob.glob('**/*.mdx', recursive=True)):
        with open(f, encoding='utf-8') as fh:
            s = fh.read()
        links = re.findall(r'\]\((/[^)#\s]+)\)', s) + re.findall(r'href="(/[^"#\s]+)"', s)
        for link in links:
            if link.startswith(('/images/', '/logo/', '/favicon')):
                continue
            if not os.path.exists(link.lstrip('/') + '.mdx'):
                fail('link', f'{f}: link quebrado {link}')


def check_cross_language_links():
    """Uma pagina de um idioma nao deve linkar para outro idioma."""
    for code, prefix in LANGS.items():
        if not prefix:
            continue
        for f in sorted(glob.glob(prefix + '**/*.mdx', recursive=True)):
            with open(f, encoding='utf-8') as fh:
                s = fh.read()
            body = s.split('---', 2)[-1]
            for link in re.findall(r'\]\((/[^)#\s]+)\)', body):
                if link.startswith(('/images/', '/logo/', '/favicon')):
                    continue
                if not link.startswith('/' + prefix.rstrip('/')):
                    fail('i18n-link', f'{f}: aponta para fora do idioma: {link}')


def check_page_parity():
    """O conjunto de paginas deve ser o mesmo nos tres idiomas."""
    def rel(prefix):
        pat = (prefix + '**/*.mdx') if prefix else '**/*.mdx'
        out = set()
        for f in glob.glob(pat, recursive=True):
            if f.startswith('snippets/') or f.startswith('scripts/'):
                continue
            if not prefix and (f.startswith('en/') or f.startswith('es/')
                               or f.startswith('pt/')):
                continue
            out.add(f[len(prefix):-4] if prefix else f[:-4])
        return out

    base = rel('')
    for code, prefix in LANGS.items():
        if not prefix:
            continue
        other = rel(prefix)
        for miss in sorted(base - other):
            fail('paridade', f'existe na raiz (pt-BR) mas falta em {code}: {miss}')
        for extra in sorted(other - base):
            fail('paridade', f'existe em {code} mas falta na raiz (pt-BR): {extra}')


def check_imports():
    for f in glob.glob('snippets/*.mdx'):
        with open(f, encoding='utf-8') as fh:
            s = fh.read()
        SNIPPET_EXPORTS['/' + f] = set(re.findall(r'export const (\w+)', s))

    known = {name: src for src, names in SNIPPET_EXPORTS.items() for name in names}
    for f in sorted(glob.glob('**/*.mdx', recursive=True)):
        if f.startswith('snippets/'):
            continue
        with open(f, encoding='utf-8') as fh:
            s = fh.read()
        imported = set()
        for m in re.finditer(r"import \{([^}]+)\} from '(/snippets/[^']+)';", s):
            imported |= {x.strip() for x in m.group(1).split(',')}
            if not os.path.exists('.' + m.group(2)):
                fail('import', f'{f}: snippet inexistente {m.group(2)}')
        body = s.split('---', 2)[-1]
        for name in known:
            used = re.search(r'<' + name + r'[\s/>]', body) or re.search(r'\{' + name + r'\}', body)
            if used and name not in imported:
                fail('import', f'{f}: usa {name} sem import')


OVERVIEW_ROW = {
    'Texto': 'TEXT',
    'Imagem': 'IMAGE',
    'Áudio': 'AUDIO',
    'Vídeo': 'VIDEO',
    'Documento': 'DOCUMENT',
    'Sticker': 'STICKER',
    'Localização': 'LOCATION',
    'Contato': 'CONTACT',
    'Botões rápidos': 'INTERACTIVE_BUTTON',
    'Botões de ação': 'INTERACTIVE_ACTION',
    'Template pré-aprovado': 'TEMPLATE',
    'Flows': 'FLOW',
    'Reação (emoji)': 'REACTION',
    'Pedir localização': 'LOCATION_REQUEST',
    'Lista de opções': 'INTERACTIVE_LIST',
    'Catálogo': 'CATALOG',
    'Produto': 'PRODUCT',
    'Multi-produto': 'PRODUCT_LIST',
    'Detalhes do pedido': 'ORDER_DETAILS',
    'Status do pedido': 'ORDER_STATUS',
}

MARK = {'yes': '✅', 'no': '❌', 'partial': '⚠️', 'unknown': '🔍'}


def snippet_matrix():
    """A matriz que a tabela de cada endpoint usa, lida do proprio snippet."""
    with open('snippets/channel-support.mdx', encoding='utf-8') as fh:
        source = fh.read()
    matrix = {}
    for name, cells in re.findall(r"(\w+): \[([^\]]+)\],", source):
        values = [v.strip().strip("'") for v in cells.split(',')]
        if len(values) == 5 and all(v in MARK for v in values):
            matrix[name] = values
    return matrix


def check_channel_matrix():
    """
    A disponibilidade por canal e dita em um lugar so.

    Antes cada pagina de endpoint declarava os canais na mao, e o snippet
    assumia "sim" para o que a pagina nao dissesse: a pagina do Flow prometia
    envio pelo WhatsApp Web e pelo Telegram, que nao existe em nenhum dos dois.
    Aqui a matriz do snippet e conferida contra as tabelas de "O que cada canal
    aceita", que sao as mesmas publicadas no painel.
    """
    matrix = snippet_matrix()
    if not matrix:
        fail('canais', 'snippets/channel-support.mdx: nao consegui ler a matriz')
        return

    for f in sorted(glob.glob('messages/send-*.mdx') + glob.glob('*/messages/send-*.mdx')):
        with open(f, encoding='utf-8') as fh:
            body = fh.read()
        used = re.search(r'<ChannelSupport([^>]*)/>', body)
        if not used:
            continue
        kind = re.search(r'type="([A-Z_]+)"', used.group(1))
        lang = re.search(r'lang="(pt|en|es)"', used.group(1))
        if not kind or kind.group(1) not in matrix:
            fail('canais', f'{f}: ChannelSupport sem type conhecido')
            continue
        expected = f.split('/')[0] if f.startswith(('en/', 'es/')) else 'pt'
        if not lang or lang.group(1) != expected:
            fail('canais', f'{f}: ChannelSupport com lang diferente da pasta')

    with open('channels/message-support.mdx', encoding='utf-8') as fh:
        overview = fh.read()

    seen = set()
    for line in overview.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) != 6 or cells[0] not in OVERVIEW_ROW:
            continue
        kind = OVERVIEW_ROW[cells[0]]
        seen.add(kind)
        if kind not in matrix:
            fail('canais', f'a pagina de canais tem {cells[0]} e o snippet nao tem {kind}')
            continue
        marks = [c[:2].strip() if c[:2].strip() in MARK.values() else c[:1] for c in cells[1:]]
        want = [MARK[v] for v in matrix[kind]]
        if marks != want:
            fail('canais', f'{kind}: a pagina de canais diz {marks} e o snippet diz {want}')

    for kind in OVERVIEW_ROW.values():
        if kind not in seen:
            fail('canais', f'a pagina de canais perdeu a linha de {kind}')


PANEL_METHODS = '../pennsylvania-lancaster/src/config/playground-methods.ts'

STATUS_LABEL = {
    'soon': {'pt': 'Em desenvolvimento.', 'en': 'In development.', 'es': 'En desarrollo.'},
    'broken': {'pt': 'Em implementação.', 'en': 'Being implemented.', 'es': 'En implementación.'},
}

"""
Estado de cada tipo de mensagem na nossa API.

`live` existe e funciona, `soon` ainda nao existe, `broken` existe e falha ou
entrega menos do que a Meta permite. Quem manda e o catalogo do painel, que e o
mesmo que alimenta o playground; esta tabela e a copia usada quando o repo do
painel nao esta ao lado, e o proprio linter avisa se as duas discordarem.
"""
METHOD_STATUS = {
    'TEXT': 'live',
    'IMAGE': 'live',
    'AUDIO': 'live',
    'VIDEO': 'live',
    'DOCUMENT': 'soon',
    'STICKER': 'live',
    'LOCATION': 'broken',
    'LOCATION_REQUEST': 'soon',
    'CONTACT': 'broken',
    'REACTION': 'soon',
    'INTERACTIVE_BUTTON': 'live',
    'INTERACTIVE_ACTION': 'live',
    'INTERACTIVE_LIST': 'soon',
    'FLOW': 'soon',
    'CATALOG': 'soon',
    'PRODUCT': 'soon',
    'PRODUCT_LIST': 'soon',
    'ORDER_DETAILS': 'soon',
    'ORDER_STATUS': 'soon',
    'TEMPLATE': 'live',
}


def panel_status():
    """O estado publicado no painel, quando o repo dele esta ao lado deste."""
    if not os.path.exists(PANEL_METHODS):
        return None
    with open(PANEL_METHODS, encoding='utf-8') as fh:
        source = fh.read()
    found = re.findall(r"id: '([A-Z_]+)',.*?status: '(\w+)'", source, re.S)
    return dict(found) if found else None


def endpoint_pages():
    """Pagina de endpoint e o tipo que ela declara, por idioma."""
    out = []
    for f in sorted(glob.glob('messages/send-*.mdx') + glob.glob('en/messages/send-*.mdx')
                    + glob.glob('es/messages/send-*.mdx')):
        with open(f, encoding='utf-8') as fh:
            body = fh.read()
        m = re.search(r'<ChannelSupport[^>]*type="([A-Z_]+)"', body)
        if m:
            lang = f.split('/')[0] if f.startswith(('en/', 'es/')) else 'pt'
            out.append((f, m.group(1), lang, body))
    return out


def check_method_status():
    """
    Pagina sem aviso promete endpoint que funciona.

    O aviso e a unica coisa que separa "ja da para integrar" de "ainda nao
    existe", e ele mora na prosa de cada pagina: esquecer um deixa a doc
    prometendo o que a API nao entrega. Aqui cada pagina e conferida contra o
    catalogo do painel, que e o mesmo que alimenta o playground.
    """
    panel = panel_status()
    if panel:
        for kind, state in METHOD_STATUS.items():
            if kind in panel and panel[kind] != state:
                fail('estado', f'{kind}: painel diz {panel[kind]} e o linter diz {state}')
        for kind in panel:
            if kind not in METHOD_STATUS:
                fail('estado', f'{kind}: existe no painel e falta na tabela do linter')

    for f, kind, lang, body in endpoint_pages():
        state = METHOD_STATUS.get(kind)
        if not state:
            fail('estado', f'{f}: tipo {kind} sem estado conhecido')
            continue
        for other, labels in STATUS_LABEL.items():
            label = f'**{labels[lang]}**'
            has = label in body
            if other == state and not has:
                fail('estado', f'{f}: {kind} e {state} e a pagina nao avisa "{labels[lang]}"')
            if other != state and has:
                fail('estado', f'{f}: {kind} e {state} e a pagina avisa "{labels[lang]}"')

        # O playground chama a API de verdade: so pode existir em pagina de
        # endpoint que existe. E o contrario tambem vale — endpoint que existe
        # sem playground e pagina que parece rascunho.
        has_playground = bool(re.search(r'^openapi:', body, re.M))
        exists = state in ('live', 'broken')
        if exists and not has_playground:
            fail('estado', f'{f}: {kind} existe na API e a pagina nao tem playground')
        if not exists and has_playground:
            fail('estado', f'{f}: {kind} ainda nao existe e a pagina tem playground')


CHANNEL_KIND_ORDER = ['WHATSAPP_OFFICIAL', 'WHATSAPP_WEB', 'INSTAGRAM', 'MESSENGER', 'TELEGRAM']


def panel_channels():
    """
    O que o painel diz sobre canal e ressalva, por tipo.

    Devolve `{tipo: (canais, ressalvas)}`. As listas do arquivo sao constantes
    (`ALL`, `COMMERCE`, ...), entao elas sao resolvidas antes.
    """
    if not os.path.exists(PANEL_METHODS):
        return None
    with open(PANEL_METHODS, encoding='utf-8') as fh:
        source = fh.read()

    consts = {}
    for name, body in re.findall(r"const (\w+): ChannelKind\[\] = ([^;]+);", source):
        consts[name] = (
            list(CHANNEL_KIND_ORDER)
            if 'CHANNEL_KINDS' in body
            else re.findall(r"'([A-Z_]+)'", body)
        )

    rows = {}
    for kind, body in re.findall(r"id: '([A-Z_]+)',(.*?)\n  \},", source, re.S):
        listed = re.search(r"channels: ([^\n]+?),?\n", body)
        if not listed:
            continue
        value = listed.group(1).strip().rstrip(',')
        channels = consts.get(value) or re.findall(r"'([A-Z_]+)'", value)
        caveats = {}
        found = re.search(r"caveats: \{([^}]*)\}", body)
        if found:
            caveats = dict(re.findall(r"(\w+): '(\w+)'", found.group(1)))
        rows[kind] = (channels, caveats)

    return rows or None


def check_matrix_vs_panel():
    """
    A doc e o playground contam a mesma historia, celula por celula.

    O painel tem tres estados por canal: aceita, aceita com ressalva
    (`caveats`) e nao aceita. A doc tem quatro marcas. Esta e a traducao entre
    os dois, e e o que impede a tabela publicada de dizer ✅ onde o playground
    diz "nao disponivel" — que foi exatamente como a pagina do Flow prometeu
    envio pelo WhatsApp Web.
    """
    panel = panel_channels()
    if not panel:
        return

    matrix = snippet_matrix()
    for kind, vals in matrix.items():
        if kind not in panel:
            fail('canais', f'{kind}: esta na doc e falta no catalogo do painel')
            continue

        channels, caveats = panel[kind]
        for index, channel in enumerate(CHANNEL_KIND_ORDER):
            caveat = caveats.get(channel)
            want = (
                'partial'
                if caveat == 'partial'
                else 'unknown'
                if caveat == 'unconfirmed'
                else 'yes'
                if channel in channels
                else 'no'
            )
            if vals[index] != want:
                fail(
                    'canais',
                    f'{kind}.{channel}: doc diz {vals[index]} e o painel diz {want}',
                )


def main():
    if not os.path.exists('docs.json'):
        print('erro: rode na raiz do repo (onde esta o docs.json)')
        return 1
    docs = load_docs()
    check_json_valid()
    check_nav(docs)
    check_orphans(docs)
    check_openapi_array(docs)
    check_openapi_frontmatter()
    check_links()
    check_cross_language_links()
    check_page_parity()
    check_imports()
    check_channel_matrix()
    check_matrix_vs_panel()
    check_method_status()

    if not problems:
        print('check-docs: tudo certo')
        return 0

    by_check = {}
    for check, msg in problems:
        by_check.setdefault(check, []).append(msg)
    for check in sorted(by_check):
        print(f'\n[{check}] {len(by_check[check])} problema(s)')
        for msg in by_check[check][:25]:
            print('  -', msg)
        if len(by_check[check]) > 25:
            print(f'  ... e {len(by_check[check]) - 25} outros')
    print(f'\ncheck-docs: {len(problems)} problema(s)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
