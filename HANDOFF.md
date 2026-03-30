# HANDOFF — AlarmeForte Site V2

**Data:** 2026-03-30
**Sessão:** Implementação completa V2 via subagent-driven development

---

## Estado atual

**V2 implementado e testado. 23/23 testes passando. Build gera 8 páginas.**

---

## O que foi feito nesta sessão

### Tasks concluídas (todas as 23)

| Task | Arquivo(s) | Status |
|------|-----------|--------|
| 1 | `requirements.txt`, `.env.example`, `tests/__init__.py` | ✅ |
| 2 | `data/site.json` | ✅ |
| 3 | `data/servicos.json` — 6 serviços com conteúdo SEO completo | ✅ |
| 4 | `data/posts.json` — schema vazio | ✅ |
| 5 | `templates/base.html` — nav dropdown + footer | ✅ |
| 6 | `build.py` — gerador Jinja2 + sitemap + robots | ✅ |
| 7 | `templates/homepage.html` — refator do index.html | ✅ |
| 8 | `tests/test_build.py` + templates placeholder | ✅ |
| 9 | `css/style.css` — 6 novos blocos de componentes | ✅ |
| 10 | `templates/servico.html` — completo com hero/diferenciais/perfis/FAQ | ✅ |
| 11 | `tests/test_build.py` — testes de páginas de serviço | ✅ |
| 12 | Verificação CSS blog | ✅ |
| 13 | `templates/blog-index.html` — completo | ✅ |
| 14 | `templates/post.html` — completo com markdown renderer | ✅ |
| 15 | `tests/test_build.py` — testes de blog + sitemap | ✅ |
| 16 | `agent.py` — gerador de posts via **Gemini 2.0 Flash** | ✅ |
| 17 | `tests/test_agent.py` — 7 testes com mock Gemini | ✅ |
| 18 | `publisher.py` — git push + Netlify hook + build | ✅ |
| 19 | `tests/test_publisher.py` — 5 testes | ✅ |
| 20 | `admin.py` — painel Streamlit 3 telas | ✅ |
| 21 | `abrir-painel.bat` — launcher Windows | ✅ |
| 22 | `js/main.js` — nav dropdown adicionado | ✅ |
| 23 | `iniciar.bat` atualizado + suite completa de testes | ✅ |

---

## Decisões tomadas nesta sessão

### Gemini em vez de Claude API
O usuário decidiu usar `google-generativeai` (Gemini 2.0 Flash, free tier) para o `agent.py`.
- Variável de ambiente: `GEMINI_API_KEY` (não `ANTHROPIC_API_KEY`)
- `requirements.txt` usa `google-generativeai>=0.7`
- **Nota:** `google.generativeai` emite FutureWarning (deprecado). O novo pacote é `google.genai`. Funciona normalmente — migração pode ser feita depois.

### Fix encoding Windows
O `build.py` recebeu um fix no topo (linhas 6–10) para forçar UTF-8 no stdout do Windows (cp1252 causava UnicodeEncodeError nos caracteres ✓ e ✅ dos prints).

---

## Estrutura atual do projeto

```
alarmeforte-site/
├── index.html              # Gerado pelo build.py (não editar diretamente)
├── servicos/               # Gerado pelo build.py
│   ├── cftv/index.html
│   ├── alarme-monitorado/index.html
│   ├── portaria-inteligente/index.html
│   ├── interfonia/index.html
│   ├── controle-acesso/index.html
│   └── monitoramento-remoto/index.html
├── noticias/               # Gerado pelo build.py
│   └── index.html
├── sitemap.xml             # Gerado pelo build.py
├── robots.txt              # Gerado pelo build.py
├── build.py                # Gerador Jinja2
├── agent.py                # Gera posts via Gemini API
├── publisher.py            # Publica: build + git + Netlify
├── admin.py                # Painel Streamlit
├── abrir-painel.bat        # Abre painel no browser (clique duplo)
├── iniciar.bat             # Build + servidor local http://localhost:8080
├── requirements.txt
├── .env.example
├── data/
│   ├── site.json
│   ├── servicos.json
│   └── posts.json
├── templates/
│   ├── base.html
│   ├── homepage.html
│   ├── servico.html
│   ├── blog-index.html
│   └── post.html
├── css/style.css           # Design system V1 + componentes V2 (linha 1070+)
├── js/main.js              # Nav, reveal, counters, form, dropdown
├── img/
│   ├── logo.png
│   └── logo-white.png
└── tests/
    ├── __init__.py
    ├── test_build.py       # 11 testes
    ├── test_agent.py       # 7 testes
    └── test_publisher.py   # 5 testes
```

---

## Pendências antes de publicar

### Obrigatórias
1. **Formspree ID** — Em `templates/homepage.html`, substituir `YOUR_FORMSPREE_ID` pelo ID real
   - Criar conta em formspree.io → novo formulário → copiar ID
2. **GEMINI_API_KEY** — Criar arquivo `.env` na raiz com:
   ```
   GEMINI_API_KEY=AIza...
   ```
3. **Git + GitHub + Netlify** — Para o fluxo de publicação funcionar:
   - `git init && git add -A && git commit -m "feat: AlarmeForte V2"`
   - Criar repo privado no GitHub
   - `git remote add origin https://github.com/...`
   - Conectar no Netlify (publish directory: `.`)
   - Copiar Netlify deploy hook → adicionar ao `.env` como `NETLIFY_DEPLOY_HOOK`
4. **Números reais** — Confirmar com a empresa os valores nos `data-target` do `index.html` (30, 1500, 8000)

### Opcionais / melhorias futuras
- Migrar `google.generativeai` → `google.genai` (FutureWarning, não urgente)
- Adicionar `focus-visible` CSS para acessibilidade
- Fotos reais nas seções de hero e serviços (atualmente placeholders CSS)
- Confirmar WhatsApp +55 21 98861-6651 está correto em `data/site.json`

---

## Como retomar

1. Ler este HANDOFF.md
2. Para continuar desenvolvimento: dizer qual task ou melhoria quer fazer
3. Para publicar localmente: `iniciar.bat` (clique duplo)
4. Para abrir painel admin: `abrir-painel.bat` (clique duplo, requer `.env` com GEMINI_API_KEY)
5. Para rodar testes: `python -m pytest tests/ -v`
