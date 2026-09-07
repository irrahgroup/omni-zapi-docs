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
