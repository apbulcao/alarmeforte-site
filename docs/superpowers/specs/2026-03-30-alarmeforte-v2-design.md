# Design Spec — AlarmeForte Site V2

**Data:** 2026-03-30
**Status:** Aprovado

---

## Contexto

V1 entregou a homepage single-page. V2 adiciona profundidade de conteúdo (6 páginas de serviço), blog com agente de geração automática, e um painel de controle simples para que o pai do proprietário possa solicitar, revisar e publicar artigos com um clique. Foco em SEO local (Rio de Janeiro) e conversão.

---

## Arquitetura

```
alarmeforte-site/
├── build.py              # Gerador Jinja2 — lê data/ + templates/ → gera HTML
├── requirements.txt      # jinja2, anthropic, gitpython, requests
├── admin.py              # Streamlit — painel de controle do blog
├── agent.py              # Agente Claude API — gera rascunhos de post
├── abrir-painel.bat      # Clique duplo → abre painel no navegador
├── iniciar.bat           # build + server local (desenvolvimento)
│
├── data/
│   ├── site.json         # Info global: tel, endereço, WhatsApp, redes sociais
│   ├── servicos.json     # Conteúdo das 6 páginas de serviço
│   └── posts.json        # Posts do blog (rascunhos + publicados)
│
├── templates/
│   ├── base.html         # Nav + footer compartilhado (template mãe)
│   ├── homepage.html     # Homepage refatorada para usar base.html
│   ├── servico.html      # Template das 6 páginas de serviço
│   ├── blog-index.html   # Grid de artigos
│   └── post.html         # Artigo individual
│
├── css/style.css         # Existente + novos componentes
├── js/main.js            # Existente
└── img/                  # Logo + imagens dos serviços
```

**Fluxo de geração:**
`data/*.json` + `templates/*.html` → `build.py` → HTML estático na raiz e em `servicos/`, `noticias/`

---

## Páginas de Serviço (6 páginas)

URLs: `/servicos/cftv/`, `/servicos/alarme-monitorado/`, `/servicos/portaria-inteligente/`, `/servicos/interfonia/`, `/servicos/controle-acesso/`, `/servicos/monitoramento-remoto/`

### Estrutura de cada página de serviço

1. **Page Hero** — título do serviço, subtítulo orientado a benefício, CTA "Solicitar Orçamento". Hero menor que o da homepage (não full-viewport).

2. **Breadcrumb** — `Início > Serviços > [Nome do Serviço]`

3. **O que é / Como funciona** — 2–3 parágrafos em linguagem simples. Foco em benefício para o cliente.

4. **Diferenciais AlarmeForte** — 3–4 cards: o que a empresa entrega além do básico (ex: monitoramento 24h por equipe própria, resposta rápida no RJ).

5. **Para quem é** — seção visual com 3 perfis: Residencial, Comercial, Condominial. Cada um com o que ganha com o serviço.

6. **Perguntas Frequentes** — 4–5 FAQs específicas do serviço, accordion expand/collapse. Otimizadas para SEO long-tail.

7. **CTA Final** — formulário simplificado ou link para seção de contato. Mensagem de urgência suave ("Diagnóstico gratuito, sem compromisso").

### Conteúdo
Gerado pelo Claude com base nos dados de `servicos.json`. Cada serviço tem campos: `titulo`, `slug`, `descricao_curta`, `meta_description`, `diferenciais[]`, `perfis[]`, `faqs[]`.

---

## Blog

### Páginas
- `/noticias/` — grid de cards com foto placeholder, título, data, resumo, link "Ler mais"
- `/noticias/[slug]/` — artigo individual: título, data, corpo com H2s, CTA no final

### `agent.py` — Geração de conteúdo
```
python agent.py --tema "câmeras para casas de veraneio no RJ"
# ou sem tema: agente escolhe baseado em SEO local
```

O agente gera via Claude API:
- Título otimizado para SEO
- `meta_description` (~155 chars)
- Artigo de ~800 palavras em PT-BR (introdução, 3–4 seções H2, conclusão + CTA AlarmeForte)
- `slug` URL limpo
- Tags, data de criação

Salva em `posts.json` com `status: rascunho`. Não publica automaticamente — aguarda aprovação no painel.

**Agendamento opcional:** Windows Task Scheduler pode rodar `agent.py` 1–2x/semana para acumular rascunhos automaticamente.

---

## Painel de Controle (`admin.py`)

Interface Streamlit para uso do pai. Aberta via `abrir-painel.bat` (sem terminal visível).

### Tela 1 — Início
- Campo de texto: "Sobre o que quer publicar?" (opcional)
- Botão "Gerar artigo" — chama `agent.py` com o tema informado
- Lista de rascunhos aguardando revisão (título + data de geração)

### Tela 2 — Revisão
- Campo editável: Título
- Área de texto editável: Conteúdo completo do artigo
- Botões: `[Descartar]` e `[✓ Publicar agora]`

### Tela 3 — Confirmação
- Mensagem: "Artigo publicado! O site será atualizado em ~30 segundos."
- Botões: `[Ver no site]` e `[Criar outro]`

### O que "Publicar" faz
1. Atualiza `status: publicado` + `data_publicacao` no `posts.json`
2. Chama `build.py` para regenerar o HTML
3. Git commit + push via `gitpython`
4. Chama Netlify deploy hook via `requests.post()`

---

## Deploy Pipeline

- **Repositório:** GitHub (privado)
- **Hospedagem:** Netlify — conectado ao GitHub, deploy automático a cada push
- **Deploy hook:** URL configurada no Netlify, chamada pelo painel ao publicar
- **Domínio:** `alarmeforte.com.br` — DNS apontando para Netlify

---

## SEO Técnico

Gerado automaticamente pelo `build.py` a partir dos dados JSON:

- `<title>` e `<meta description>` únicos por página
- `<h1>` alinhado com o título SEO
- `sitemap.xml` com todas as URLs (homepage + serviços + posts publicados)
- `robots.txt` padrão
- URLs limpas: `/servicos/cftv/index.html` servida como `/servicos/cftv/`
- **Schema markup JSON-LD** em páginas de serviço: `LocalBusiness` + `Service` — fator de ranking local para Rio de Janeiro
- Open Graph tags para compartilhamento social

---

## CSS — Novos Componentes

Adicionados ao `style.css` existente sem quebrar o V1:

| Classe | Uso |
|---|---|
| `.page-hero` | Hero menor para páginas internas |
| `.breadcrumb` | Navegação contextual |
| `.faq-accordion` | Perguntas frequentes com expand/collapse |
| `.blog-grid` | Grid de cards de artigo |
| `.post-content` | Tipografia do corpo de artigo |
| `.nav-dropdown` | Submenu "Serviços" no nav |

---

## Design Visual

Stitch será usado para gerar mockups das novas páginas antes da implementação:
- Página de serviço (template)
- Blog index
- Artigo individual
- Painel admin (Streamlit)

Design system "Fortaleza" do V1 mantido: `#080E09` dark bg, `#1F693A` verde primário, `#84C25B` acento, EB Garamond + DM Sans.

---

## Imagens e Mídia

- **Páginas de serviço:** imagens ilustrativas via CSS gradients/placeholders no lançamento. Substituição por fotos reais em momento posterior, sem alterar estrutura.
- **Cards do blog:** foto de capa opcional. Se ausente, card exibe placeholder visual com cor do design system.
- **Logo e identidade:** `img/logo.png` e `img/logo-white.png` já existem do V1.

---

## Fora do Escopo V2

- Páginas de produto por equipamento/marca
- Área do cliente / login
- Integração com CRM (`crm-alarmeforte/` é projeto separado)
- WhatsApp API / automação de mensagens
- Publicação automática sem revisão humana

---

## Verificação

1. `python build.py` → gera todos os HTML sem erros
2. `iniciar.bat` → homepage carrega em localhost
3. Navegar nas 6 páginas de serviço — nav e footer consistentes
4. Clicar em "Gerar artigo" no painel → rascunho aparece na lista
5. Editar e publicar um post → commit no GitHub → deploy no Netlify em ~30s
6. `sitemap.xml` lista todas as URLs
7. Testar mobile (Chrome DevTools) em todas as páginas novas
