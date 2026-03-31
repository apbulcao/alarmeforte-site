# HANDOFF — AlarmeForte Site V2

**Data:** 2026-03-31
**Sessão:** Paleta de cores, fotos de produto e fix do dropdown

---

## Estado atual

**Site no ar em https://alarmeforte-site.netlify.app**
Deploy automático via GitHub → Netlify a cada push no branch `master`.

---

## O que foi feito nesta sessão

### Paleta de cores
- Dark background atualizado de `#080E09` (quase preto) para `#092A15` (verde escuro, igual ao site original alarmeforte.com.br)
- Aplicado em 5 pontos do CSS: variável root, navbar scrolled, mobile menu, dropdown, `<select>` do formulário
- Verdes primários (`#1F693A` e `#84C25B`) eram idênticos ao original — não mudaram

### Fix do dropdown (concluído)
- Trocada a bridge `::before` pela abordagem `padding-top: 14px` + `top: 100%`
- O menu começa imediatamente abaixo do botão (sem gap real), eliminando edge case de movimentos diagonais rápidos

### Fotos de produto nas páginas de serviço
- Campo `imagem` + `imagem_alt` adicionado nos 6 serviços em `data/servicos.json`
- Imagens apontam para o CDN do site original (alarmeforte.com.br/wp-content/uploads/)
- Template `servico.html` atualizado com layout split 50/50 (texto + foto) quando imagem existe
- No mobile cai para coluna única com aspect-ratio 16:9
- Hover faz zoom suave de 3% na imagem

**Mapeamento de imagens por serviço:**
| Serviço | Imagem |
|---------|--------|
| CFTV | cameras-1.webp |
| Alarme Monitorado | products-1024x361.png.webp |
| Portaria Inteligente | PHOTO-2021-06-17-13-38-39-3.webp |
| Interfonia | tvip-3000-wifi-tecnologia-wifi.jpg.webp |
| Controle de Acesso | controlador-de-acesso-facial-ss-7530-face...webp |
| Monitoramento Remoto | casa-segura.png.webp |

### Setup de produção (sessão anterior)
- `templates/homepage.html` — Formspree ID: `mzdkrook`
- `.env` criado com `GEMINI_API_KEY`
- Push para GitHub: `https://github.com/apbulcao/alarmeforte-site`
- Netlify conectado ao repo, deploy automático ativo
- Counter de clientes: `data-target="300"` (303 clientes recorrentes no CRM)

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
│   ├── servicos.json       # Campo imagem adicionado em todos os serviços
│   └── posts.json
├── templates/
│   ├── base.html
│   ├── homepage.html       # Formspree ID: mzdkrook
│   ├── servico.html        # Layout split com imagem de produto
│   ├── blog-index.html
│   └── post.html
├── css/style.css           # Dark bg: #092A15; .servico-split adicionado
├── js/main.js
├── img/
└── tests/                  # 23 testes passando
```

---

## Design System (atual)

- Background dark: `#092A15` | Verde primário: `#1F693A` | Acento: `#84C25B`
- Display font: EB Garamond | Body font: DM Sans
- Conceito: "Fortaleza" — autoridade, tradição, confiança

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

- Conectar domínio `alarmeforte.com.br` no Netlify (Domain management)
- Migrar `google.generativeai` → `google.genai` (FutureWarning, não urgente)
- Confirmar números: fundada 1992 = 33 anos (não 30), e 8.000 pontos de monitoramento
- Adicionar `focus-visible` CSS para acessibilidade
- Fotos próprias da empresa para substituir as do CDN do WordPress original

---

## Como retomar

1. Ler este HANDOFF.md
2. Servidor local: `iniciar.bat`
3. Painel admin: `abrir-painel.bat` (requer `.env` com GEMINI_API_KEY)
4. Testes: `python -m pytest tests/ -v`
5. Deploy: editar → `python build.py` → `git commit` → `git push` → Netlify redeploya automaticamente
