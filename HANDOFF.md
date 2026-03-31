# HANDOFF — AlarmeForte Site V2

**Data:** 2026-03-31
**Sessão:** Paleta de cores, fotos de produto e fix do dropdown

---

## Estado atual

**Site no ar em https://alarmeforte-site.netlify.app**
Deploy automático via GitHub → Netlify a cada push no branch `master`.

---

## O que foi feito nesta sessão

### Bugs corrigidos
1. **Dropdown de navegação** — menu de serviços desaparecia ao mover o mouse do botão para os itens. Fix: `padding-top: 14px` + `top: 100%` no `.nav-dropdown-menu` (abordagem mais robusta que bridge `::before`). **Pendente aplicar o fix final do code reviewer** — ver nota abaixo.
2. **Cards "Para quem é"** — hover tornava fundo branco e título invisível porque seção usa `section-light` mas card foi estilizado para fundo escuro. Fix: hover usa `background: var(--green-primary)` (verde sólido).

### Setup de produção concluído
- `templates/homepage.html` — Formspree ID substituído: `mzdkrook`
- `.env` criado com `GEMINI_API_KEY` (chave do `.openclaw/.env`)
- Git inicializado, `.gitignore` adicionado (`.env` e `__pycache__` excluídos)
- Push para GitHub: `https://github.com/apbulcao/alarmeforte-site`
- Netlify conectado ao repo, site publicado: `alarmeforte-site.netlify.app`
- Counter de clientes atualizado: `data-target="300"` (303 clientes recorrentes no CRM)

---

## Pendência técnica do dropdown

O code reviewer recomendou trocar a bridge `::before` pela abordagem `padding-top`. A correção atual (bridge) funciona no caminho feliz mas tem edge case em movimentos diagonais rápidos.

**Fix recomendado em `css/style.css`:**
```css
.nav-dropdown-menu {
  top: 100%;           /* era: calc(100% + 14px) */
  padding-top: 14px;   /* cria o espaço visual internamente */
  /* remover o ::before após aplicar */
}
```
E remover o bloco `.nav-dropdown-menu::before { ... }` logo abaixo.

---

## Estrutura atual do projeto

```
alarmeforte-site/
├── index.html              # Gerado pelo build.py
├── servicos/               # 6 páginas de serviço geradas
├── noticias/index.html     # Blog gerado
├── sitemap.xml / robots.txt
├── build.py                # Gerador Jinja2
├── agent.py                # Gera posts via Gemini API
├── publisher.py            # Build + git push (Netlify via CD automático)
├── admin.py                # Painel Streamlit
├── abrir-painel.bat        # Abre painel admin
├── iniciar.bat             # Build + servidor local http://localhost:8080
├── .env                    # GEMINI_API_KEY preenchida; NETLIFY_DEPLOY_HOOK vazio
├── requirements.txt
├── data/
│   ├── site.json
│   ├── servicos.json
│   └── posts.json
├── templates/
│   ├── base.html
│   ├── homepage.html       # Formspree ID: mzdkrook
│   ├── servico.html
│   ├── blog-index.html
│   └── post.html
├── css/style.css
├── js/main.js
├── img/
└── tests/                  # 23 testes passando
```

---

## Infraestrutura

| Serviço | URL / Info |
|---------|-----------|
| Site ao vivo | https://alarmeforte-site.netlify.app |
| GitHub | https://github.com/apbulcao/alarmeforte-site |
| Netlify | app.netlify.com → team Alarmeforte → projeto alarmeforte-site |
| Formspree | https://formspree.io/f/mzdkrook |

---

## Pendências restantes

### Opcionais / melhorias futuras
- Conectar domínio `alarmeforte.com.br` no Netlify (Domain management)
- Migrar `google.generativeai` → `google.genai` (FutureWarning, não urgente)
- Confirmar números: 30 anos (fundada 1992 = 33 anos), 8.000 pontos de monitoramento
- Adicionar `focus-visible` CSS para acessibilidade

---

## Como retomar

1. Ler este HANDOFF.md
2. Servidor local: `iniciar.bat`
3. Painel admin: `abrir-painel.bat` (requer `.env` com GEMINI_API_KEY)
4. Testes: `python -m pytest tests/ -v`
5. Deploy: editar → `build.py` → `git commit` → `git push` → Netlify redeploya automaticamente
