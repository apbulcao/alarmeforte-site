"""Smoke tests para build.py."""
import json
import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).parent.parent


def run_build():
    result = subprocess.run(
        ['python', 'build.py'],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    return result


def test_build_exits_successfully():
    result = run_build()
    assert result.returncode == 0, f"build.py falhou:\n{result.stderr}"


def test_build_creates_homepage():
    run_build()
    assert (ROOT / 'index.html').exists()


def test_homepage_contains_alarmeforte():
    run_build()
    content = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert 'AlarmeForte' in content


def test_build_creates_sitemap():
    run_build()
    assert (ROOT / 'sitemap.xml').exists()
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    assert 'alarmeforte.com.br' in sitemap


def test_build_creates_robots():
    run_build()
    assert (ROOT / 'robots.txt').exists()


def test_build_creates_all_service_pages():
    run_build()
    servicos_data = json.loads((ROOT / 'data' / 'servicos.json').read_text(encoding='utf-8'))
    for s in servicos_data['servicos']:
        page = ROOT / 'servicos' / s['slug'] / 'index.html'
        assert page.exists(), f"Página de serviço não gerada: {s['slug']}"


def test_service_page_has_seo_elements():
    run_build()
    page = (ROOT / 'servicos' / 'cftv' / 'index.html').read_text(encoding='utf-8')
    assert 'Sistema de CFTV no Rio de Janeiro | AlarmeForte' in page
    assert 'application/ld+json' in page
    assert 'breadcrumb' in page
    assert 'faq-list' in page


def test_service_page_has_all_sections():
    run_build()
    page = (ROOT / 'servicos' / 'alarme-monitorado' / 'index.html').read_text(encoding='utf-8')
    assert 'Alarme Monitorado 24h' in page
    assert 'feature-card' in page   # diferenciais
    assert 'perfil-card' in page    # perfis
    assert 'faq-question' in page   # FAQs


def test_build_creates_blog_index():
    run_build()
    assert (ROOT / 'noticias' / 'index.html').exists()


def test_blog_index_shows_empty_state_when_no_posts():
    run_build()
    content = (ROOT / 'noticias' / 'index.html').read_text(encoding='utf-8')
    assert 'AlarmeForte' in content
    # Com posts.json vazio, página deve existir sem erro


def test_sitemap_includes_blog():
    run_build()
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    assert '/noticias/' in sitemap
    assert '/servicos/cftv/' in sitemap
    assert '/servicos/monitoramento-remoto/' in sitemap
