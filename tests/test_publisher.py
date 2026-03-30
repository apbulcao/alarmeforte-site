"""Tests para publisher.py."""
import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

import publisher


SAMPLE_DRAFT = {
    'slug': 'test-post',
    'titulo': 'Post de Teste',
    'meta_description': 'Descrição.',
    'resumo': 'Resumo.',
    'conteudo': '## Seção\n\nTexto.',
    'tags': ['teste'],
    'status': 'rascunho',
    'data_criacao': '2026-01-01',
    'data_publicacao': None
}


def setup_posts_file(tmp_path, posts=None):
    posts_dir = tmp_path / 'data'
    posts_dir.mkdir()
    posts_file = posts_dir / 'posts.json'
    posts_file.write_text(
        json.dumps({'posts': posts or [dict(SAMPLE_DRAFT)]}),
        encoding='utf-8'
    )
    return posts_file


def test_publish_post_updates_status(tmp_path, monkeypatch):
    setup_posts_file(tmp_path)
    monkeypatch.setattr(publisher, 'ROOT', tmp_path)

    with patch('publisher.subprocess.run'), patch('publisher.requests.post'):
        post = publisher.publish_post('test-post')

    assert post['status'] == 'publicado'
    assert post['data_publicacao'] is not None

    saved = json.loads((tmp_path / 'data' / 'posts.json').read_text())
    assert saved['posts'][0]['status'] == 'publicado'


def test_publish_post_raises_for_missing_slug(tmp_path, monkeypatch):
    setup_posts_file(tmp_path)
    monkeypatch.setattr(publisher, 'ROOT', tmp_path)

    with patch('publisher.subprocess.run'), patch('publisher.requests.post'):
        with pytest.raises(ValueError, match="não encontrado"):
            publisher.publish_post('slug-inexistente')


def test_discard_post_removes_from_json(tmp_path, monkeypatch):
    setup_posts_file(tmp_path)
    monkeypatch.setattr(publisher, 'ROOT', tmp_path)

    publisher.discard_post('test-post')

    saved = json.loads((tmp_path / 'data' / 'posts.json').read_text())
    assert len(saved['posts']) == 0


def test_get_drafts_returns_only_drafts(tmp_path, monkeypatch):
    posts = [
        dict(SAMPLE_DRAFT),
        {**SAMPLE_DRAFT, 'slug': 'publicado', 'status': 'publicado', 'data_publicacao': '2026-01-02'}
    ]
    setup_posts_file(tmp_path, posts)
    monkeypatch.setattr(publisher, 'ROOT', tmp_path)

    drafts = publisher.get_drafts()
    assert len(drafts) == 1
    assert drafts[0]['slug'] == 'test-post'


def test_update_post_content(tmp_path, monkeypatch):
    setup_posts_file(tmp_path)
    monkeypatch.setattr(publisher, 'ROOT', tmp_path)

    publisher.update_post_content('test-post', 'Novo Título', 'Novo conteúdo.')

    saved = json.loads((tmp_path / 'data' / 'posts.json').read_text(encoding='utf-8'))
    assert saved['posts'][0]['titulo'] == 'Novo Título'
    assert saved['posts'][0]['conteudo'] == 'Novo conteúdo.'
