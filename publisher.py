"""
publisher.py — AlarmeForte V2
Publica um post: atualiza posts.json, rebuilda o site, faz git push, aciona Netlify.
Usado pelo admin.py (Streamlit).
"""
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent


def _load_posts() -> dict:
    return json.loads((ROOT / 'data' / 'posts.json').read_text(encoding='utf-8'))  # noqa: E501


def _save_posts(data: dict) -> None:
    (ROOT / 'data' / 'posts.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def publish_post(slug: str) -> dict:
    """
    Publica um post rascunho:
    1. Atualiza status e data_publicacao em posts.json
    2. Rebuilda o site com build.py
    3. Git add + commit + push
    4. Aciona Netlify deploy hook (se configurado)
    Retorna o post publicado.
    """
    data = _load_posts()
    post = next((p for p in data['posts'] if p['slug'] == slug), None)
    if not post:
        raise ValueError(f"Post '{slug}' não encontrado em posts.json")

    post['status'] = 'publicado'
    post['data_publicacao'] = datetime.now().strftime('%Y-%m-%d')
    _save_posts(data)

    # Rebuild
    subprocess.run(['python', 'build.py'], cwd=ROOT, check=True, capture_output=True)

    # Git
    subprocess.run(['git', 'add', '-A'], cwd=ROOT, check=True, capture_output=True)
    subprocess.run(
        ['git', 'commit', '-m', f'post: {post["titulo"]}'],
        cwd=ROOT, check=True, capture_output=True
    )
    subprocess.run(['git', 'push'], cwd=ROOT, check=True, capture_output=True)

    # Netlify deploy hook
    hook_url = os.getenv('NETLIFY_DEPLOY_HOOK')
    if hook_url:
        try:
            requests.post(hook_url, timeout=10)
        except requests.RequestException:
            pass  # Deploy hook falhou — git push já garante deploy via CI

    return post


def update_post_content(slug: str, titulo: str, conteudo: str) -> None:
    """Atualiza título e conteúdo de um rascunho antes de publicar."""
    data = _load_posts()
    post = next((p for p in data['posts'] if p['slug'] == slug), None)
    if not post:
        raise ValueError(f"Post '{slug}' não encontrado")
    post['titulo'] = titulo
    post['conteudo'] = conteudo
    _save_posts(data)


def discard_post(slug: str) -> None:
    """Remove um rascunho de posts.json."""
    data = _load_posts()
    data['posts'] = [p for p in data['posts'] if p['slug'] != slug]
    _save_posts(data)


def get_drafts() -> list:
    """Retorna lista de posts com status 'rascunho'."""
    data = _load_posts()
    return [p for p in data['posts'] if p.get('status') == 'rascunho']
