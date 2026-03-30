"""
build.py — AlarmeForte V2
Gera todo o HTML estático a partir de data/*.json + templates/*.html
Uso: python build.py
"""
import sys
import io
# Força UTF-8 no stdout para evitar erros em terminais Windows (cp1252)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
from datetime import date

ROOT = Path(__file__).parent


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def render(env: Environment, template_name: str, output_path: Path, context: dict) -> None:
    template = env.get_template(template_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.render(**context), encoding='utf-8')
    print(f'  ✓ {output_path.relative_to(ROOT)}')


def generate_sitemap(root: Path, servicos: list, posts: list, site: dict) -> None:
    base = site['url'].rstrip('/')
    urls = [
        f'{base}/',
        f'{base}/noticias/',
    ]
    for s in servicos:
        urls.append(f"{base}/servicos/{s['slug']}/")
    for p in posts:
        urls.append(f"{base}/noticias/{p['slug']}/")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.append(f'  <url><loc>{url}</loc></url>')
    lines.append('</urlset>')

    (root / 'sitemap.xml').write_text('\n'.join(lines), encoding='utf-8')
    print('  ✓ sitemap.xml')


def generate_robots(root: Path, site: dict) -> None:
    content = f"User-agent: *\nAllow: /\nSitemap: {site['url'].rstrip('/')}/sitemap.xml\n"
    (root / 'robots.txt').write_text(content, encoding='utf-8')
    print('  ✓ robots.txt')


def build() -> None:
    env = Environment(
        loader=FileSystemLoader(ROOT / 'templates'),
        autoescape=True
    )

    site = load_json('data/site.json')
    servicos = load_json('data/servicos.json')['servicos']
    all_posts = load_json('data/posts.json')['posts']
    posts = [p for p in all_posts if p.get('status') == 'publicado']

    ctx_base = {'site': site, 'servicos': servicos}

    print('\nBuilding AlarmeForte V2...')

    # Homepage
    render(env, 'homepage.html', ROOT / 'index.html',
           {**ctx_base, 'posts_recentes': posts[:3]})

    # Service pages
    for servico in servicos:
        output = ROOT / 'servicos' / servico['slug'] / 'index.html'
        render(env, 'servico.html', output, {**ctx_base, 'servico': servico})

    # Blog index
    render(env, 'blog-index.html', ROOT / 'noticias' / 'index.html',
           {**ctx_base, 'posts': posts})

    # Individual posts
    for post in posts:
        output = ROOT / 'noticias' / post['slug'] / 'index.html'
        render(env, 'post.html', output, {**ctx_base, 'post': post})

    # SEO files
    generate_sitemap(ROOT, servicos, posts, site)
    generate_robots(ROOT, site)

    total = 1 + len(servicos) + 1 + len(posts)
    print(f'\n✅ Build completo — {total} páginas geradas\n')


if __name__ == '__main__':
    build()
