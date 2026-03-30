"""Tests para agent.py."""
import json
import os
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Garante que a API key fake está disponível antes do import do agent
os.environ.setdefault('GEMINI_API_KEY', 'fake-key')

from agent import slugify, generate_post, save_draft


def test_slugify_removes_accents():
    assert slugify('Câmeras de Segurança') == 'cameras-de-seguranca'


def test_slugify_handles_spaces():
    assert slugify('Rio de Janeiro RJ') == 'rio-de-janeiro-rj'


def test_slugify_max_length():
    long = 'a' * 100
    assert len(slugify(long)) <= 80


def test_generate_post_returns_required_fields():
    mock_content = json.dumps({
        'titulo': 'Câmeras para Condomínios no Rio de Janeiro',
        'meta_description': 'Guia completo sobre câmeras de segurança para condomínios no Rio de Janeiro.',
        'resumo': 'Saiba como escolher o sistema de câmeras certo para o seu condomínio.',
        'conteudo': '## Introdução\n\nTexto do artigo.\n\n## Conclusão\n\nFale com a AlarmeForte.',
        'tags': ['câmeras', 'condomínio', 'Rio de Janeiro']
    })

    mock_response = MagicMock()
    mock_response.text = mock_content

    with patch('agent.genai.GenerativeModel') as mock_model_cls:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model

        post = generate_post('câmeras para condomínios')

    assert post['titulo'] == 'Câmeras para Condomínios no Rio de Janeiro'
    assert post['status'] == 'rascunho'
    assert post['data_publicacao'] is None
    assert 'slug' in post
    assert isinstance(post['tags'], list)


def test_generate_post_handles_json_in_code_block():
    mock_content = '```json\n{"titulo": "Teste", "meta_description": "Desc", "resumo": "Resumo", "conteudo": "## H2\\n\\nTexto.", "tags": ["t"]}\n```'

    mock_response = MagicMock()
    mock_response.text = mock_content

    with patch('agent.genai.GenerativeModel') as mock_model_cls:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model

        post = generate_post('qualquer tema')

    assert post['titulo'] == 'Teste'


def test_save_draft_writes_to_posts_json(tmp_path):
    posts_file = tmp_path / 'data' / 'posts.json'
    posts_file.parent.mkdir()
    posts_file.write_text('{"posts": []}', encoding='utf-8')

    post = {
        'slug': 'test-post',
        'titulo': 'Test',
        'meta_description': 'desc',
        'resumo': 'resumo',
        'conteudo': 'texto',
        'tags': [],
        'status': 'rascunho',
        'data_criacao': '2026-01-01',
        'data_publicacao': None
    }

    import agent
    original_root = agent.ROOT
    agent.ROOT = tmp_path
    try:
        save_draft(post)
    finally:
        agent.ROOT = original_root

    saved = json.loads(posts_file.read_text(encoding='utf-8'))
    assert len(saved['posts']) == 1
    assert saved['posts'][0]['slug'] == 'test-post'


def test_save_draft_replaces_existing_slug(tmp_path):
    posts_file = tmp_path / 'data' / 'posts.json'
    posts_file.parent.mkdir()
    posts_file.write_text(json.dumps({'posts': [{'slug': 'test-post', 'titulo': 'Old', 'status': 'rascunho', 'data_criacao': '2026-01-01', 'data_publicacao': None, 'tags': [], 'conteudo': '', 'resumo': '', 'meta_description': ''}]}), encoding='utf-8')

    post = {'slug': 'test-post', 'titulo': 'New', 'meta_description': '', 'resumo': '', 'conteudo': '', 'tags': [], 'status': 'rascunho', 'data_criacao': '2026-01-02', 'data_publicacao': None}

    import agent
    original_root = agent.ROOT
    agent.ROOT = tmp_path
    try:
        save_draft(post)
    finally:
        agent.ROOT = original_root

    saved = json.loads(posts_file.read_text(encoding='utf-8'))
    assert len(saved['posts']) == 1
    assert saved['posts'][0]['titulo'] == 'New'
