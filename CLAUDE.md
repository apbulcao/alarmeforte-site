# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é
Site institucional da AlarmeForte — empresa de segurança eletrônica no Rio de Janeiro, fundada em 1992. Homepage single-page scrollable com formulário de contato funcional.

## Quick Start
```
iniciar.bat       → abre http://localhost:8080 (usa python -m http.server)
```
Sem build step, sem dependências — HTML/CSS/JS puro.

## Estrutura
```
alarmeforte-site/
├── index.html        # Homepage completa (única página V1)
├── css/style.css     # Todos os estilos (variáveis, seções, responsivo)
├── js/main.js        # Nav, reveal, counters, form, anchor scroll
├── img/              # Imagens (adicionar fotos reais aqui)
└── iniciar.bat       # Servidor local Windows
```

## Seções (em ordem no HTML)
1. `#hero` — Full-viewport dark, headline EB Garamond, badge "30 anos"
2. `#servicos` — Grid 3×2 de cards de serviço (fundo branco)
3. `#sobre` — "Por que AlarmeForte?" — 4 feature cards (fundo escuro)
4. `#numeros` — Contadores animados: 30+, 1500+, 8000+, 24h
5. `#como-funciona` — 3 steps (fundo claro)
6. `#contato` — Formulário Formspree + info de contato (fundo escuro)
7. `footer` — Links, contato, copyright

## Design System
- Background dark: `#092A15` | Verde primário: `#1F693A` | Acento: `#84C25B`
- Display font: EB Garamond | Body font: DM Sans
- Conceito: "Fortaleza" — autoridade, tradição, confiança
- Todas as variáveis CSS estão em `:root` no `style.css`

## Configuração do Formulário (NECESSÁRIA antes de usar)
No `index.html`, linha do `<form action="...">`:
1. Criar conta em formspree.io
2. Criar novo formulário → copiar o ID (formato: `xyzabcde`)
3. Substituir `YOUR_FORMSPREE_ID` pelo ID real
4. O JS bloqueia o envio e avisa se o ID não foi configurado

## Números das Estatísticas
Os números atuais (30, 1500, 8000) são estimativas conservadoras.
Confirmar com a empresa e atualizar os atributos `data-target` no `index.html`.

## Deploy (Netlify — recomendado)
1. Acesse app.netlify.com → Add new site → Deploy manually
2. Arraste a pasta `alarmeforte-site/` para o deploy area
3. Netlify gera URL automática; conectar domínio alarmeforte.com.br nas DNS settings
