"""
agent.py — AlarmeForte V2
Gera rascunhos de post para o blog via Gemini API.
Uso: python agent.py --tema "câmeras para casas de veraneio no RJ"
     python agent.py  (gera tema automaticamente)
"""
import google.generativeai as genai
import argparse
import json
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


def slugify(text: str) -> str:
    """Converte texto para slug URL-safe."""
    text = unicodedata.normalize('NFD', text.lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:80]


def generate_post(tema: str | None = None) -> dict:
    """Gera um post completo via Gemini API. Retorna dict com os campos do post."""
    if not tema:
        tema = "segurança eletrônica no Rio de Janeiro"

    prompt = f"""Você é especialista em segurança eletrônica e copywriter SEO sênior.
Escreva um artigo completo para o blog da AlarmeForte, empresa de segurança eletrônica no Rio de Janeiro desde 1992.

Tema: {tema}

Responda APENAS com um JSON válido, sem texto antes ou depois, neste formato exato:
{{
  "titulo": "título do artigo otimizado para SEO (máx 65 chars)",
  "meta_description": "descrição para SEO, máx 155 chars, inclua 'Rio de Janeiro'",
  "resumo": "resumo de 1-2 frases para o card do blog (máx 120 chars)",
  "conteudo": "artigo completo em markdown, ~800 palavras. Use ## para H2. Sem título no início. Termine com parágrafo de CTA mencionando AlarmeForte e diagnóstico gratuito.",
  "tags": ["tag1", "tag2", "tag3"]
}}

Regras:
- Português brasileiro, tom profissional e acessível
- Mencione Rio de Janeiro naturalmente
- 3 a 5 seções H2 com conteúdo prático
- Conteúdo original, não genérico
- Não use listas em excesso — prefira parágrafos"""

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Extrai JSON se vier em bloco de código
    if '```' in raw:
        match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', raw)
        if match:
            raw = match.group(1)

    data = json.loads(raw)

    return {
        'slug': slugify(data['titulo']),
        'titulo': data['titulo'],
        'meta_description': data['meta_description'],
        'resumo': data['resumo'],
        'conteudo': data['conteudo'],
        'tags': data.get('tags', []),
        'status': 'rascunho',
        'data_criacao': datetime.now().strftime('%Y-%m-%d'),
        'data_publicacao': None,
    }


def save_draft(post: dict) -> dict:
    """Salva rascunho em data/posts.json. Substitui se mesmo slug já existe."""
    posts_file = ROOT / 'data' / 'posts.json'
    data = json.loads(posts_file.read_text(encoding='utf-8'))

    # Remove rascunho anterior com mesmo slug, se houver
    data['posts'] = [p for p in data['posts'] if p['slug'] != post['slug']]
    data['posts'].insert(0, post)

    posts_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    return post


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gera rascunho de post para o blog AlarmeForte.')
    parser.add_argument('--tema', type=str, default=None, help='Tema do artigo')
    args = parser.parse_args()

    print(f'Gerando artigo: "{args.tema or "tema automatico"}"...')
    post = generate_post(args.tema)
    save_draft(post)
    print(f'Rascunho salvo: "{post["titulo"]}" (slug: {post["slug"]})')
