# AlarmeForte V2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar a homepage single-page do V1 em um site multi-página com 6 páginas de serviço, blog, agente de geração de conteúdo via Claude API, e painel de admin Streamlit para publicação com um clique.

**Architecture:** `build.py` usa Jinja2 para gerar HTML estático a partir de `data/*.json` + `templates/*.html`. `agent.py` gera rascunhos de post via Claude API. `publisher.py` faz git commit+push e aciona Netlify deploy hook. `admin.py` (Streamlit) é a interface do pai — ele pede um tema, revisa o rascunho e aperta "Publicar".

**Tech Stack:** Python 3.x, Jinja2, anthropic SDK, gitpython, requests, streamlit, python-dotenv, pytest

---

## File Map

| Arquivo | Ação | Responsabilidade |
|---------|------|-----------------|
| `requirements.txt` | Criar | Dependências Python do projeto |
| `.env.example` | Criar | Template das variáveis de ambiente |
| `data/site.json` | Criar | Info global (tel, WhatsApp, URL base) |
| `data/servicos.json` | Criar | Conteúdo completo das 6 páginas de serviço |
| `data/posts.json` | Criar | Schema inicial do blog (vazio) |
| `templates/base.html` | Criar | Nav + footer + head comum — template mãe |
| `templates/homepage.html` | Criar | Homepage refatorada para usar base.html |
| `templates/servico.html` | Criar | Template das páginas de serviço |
| `templates/blog-index.html` | Criar | Grid de artigos do blog |
| `templates/post.html` | Criar | Artigo individual |
| `build.py` | Criar | Gerador Jinja2 — gera todo o HTML estático |
| `agent.py` | Criar | Gera rascunho de post via Claude API |
| `publisher.py` | Criar | Git commit+push + Netlify deploy hook |
| `admin.py` | Criar | Painel Streamlit para o pai |
| `abrir-painel.bat` | Criar | Launcher do painel (clique duplo) |
| `css/style.css` | Modificar | Adicionar novos componentes CSS |
| `js/main.js` | Modificar | Adicionar comportamento dropdown nav |
| `iniciar.bat` | Modificar | Rodar build antes de subir servidor |
| `tests/test_build.py` | Criar | Smoke tests do build system |
| `tests/test_agent.py` | Criar | Tests do agente de conteúdo |
| `tests/test_publisher.py` | Criar | Tests do fluxo de publicação |

---

## Task 1: Setup do projeto

**Files:**
- Criar: `requirements.txt`
- Criar: `.env.example`
- Criar: `tests/__init__.py`

- [ ] **Step 1: Criar requirements.txt**

```
jinja2>=3.1
anthropic>=0.25
gitpython>=3.1
requests>=2.31
streamlit>=1.32
python-dotenv>=1.0
pytest>=8.0
```

- [ ] **Step 2: Criar .env.example**

```
ANTHROPIC_API_KEY=sk-ant-...
NETLIFY_DEPLOY_HOOK=https://api.netlify.com/build_hooks/SEU_HOOK_ID
```

- [ ] **Step 3: Criar pastas necessárias**

```bash
mkdir data templates tests
type nul > tests\__init__.py
```

- [ ] **Step 4: Instalar dependências**

```bash
pip install -r requirements.txt
```

Saída esperada: linha `Successfully installed` sem erros.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .env.example tests/
git commit -m "chore: setup V2 project structure"
```

---

## Task 2: data/site.json

**Files:**
- Criar: `data/site.json`

- [ ] **Step 1: Criar data/site.json**

```json
{
  "nome": "AlarmeForte",
  "slogan": "30 anos protegendo o Rio de Janeiro",
  "telefone": "(21) 3890-4336",
  "telefone_link": "+552138904336",
  "whatsapp": "+5521988616651",
  "whatsapp_mensagem": "Olá! Gostaria de solicitar um orçamento.",
  "email": "contato@alarmeforte.com.br",
  "cidade": "Rio de Janeiro, RJ",
  "endereco": "Rio de Janeiro, RJ",
  "ano_fundacao": 1992,
  "url": "https://alarmeforte.com.br",
  "politica_privacidade": "https://alarmeforte.com.br/politica-de-privacidade/"
}
```

- [ ] **Step 2: Commit**

```bash
git add data/site.json
git commit -m "data: add site.json global config"
```

---

## Task 3: data/servicos.json

**Files:**
- Criar: `data/servicos.json`

Este é o arquivo de conteúdo mais importante do V2. Contém os dados completos das 6 páginas de serviço.

- [ ] **Step 1: Criar data/servicos.json**

```json
{
  "servicos": [
    {
      "titulo": "Sistema de CFTV",
      "slug": "cftv",
      "meta_title": "Sistema de CFTV no Rio de Janeiro | AlarmeForte",
      "meta_description": "Câmeras de segurança HD com monitoramento remoto para residências, empresas e condomínios no Rio de Janeiro. Instalação profissional desde 1992. Orçamento gratuito.",
      "hero_subtitulo": "Câmeras HD com acesso remoto 24h via celular — para sua residência, empresa ou condomínio no Rio de Janeiro.",
      "descricao": [
        "O sistema de CFTV (Circuito Fechado de TV) é a solução mais eficaz para monitorar e registrar o que acontece no seu patrimônio em tempo real. Com câmeras de alta definição instaladas estrategicamente, você acompanha tudo de onde estiver — pelo celular, tablet ou computador.",
        "A AlarmeForte projeta e instala sistemas de CFTV desde 1992, com câmeras analógicas e IP de última geração. Cada projeto é desenvolvido sob medida: analisamos os pontos cegos, a iluminação e as necessidades específicas do local antes de qualquer instalação.",
        "Além das câmeras, oferecemos gravadores digitais (DVR/NVR) com armazenamento local e backup em nuvem — garantindo que as imagens estejam disponíveis mesmo em caso de tentativa de sabotagem do equipamento."
      ],
      "diferenciais": [
        {
          "titulo": "Projeto personalizado",
          "descricao": "Visitamos o local antes da instalação para identificar os pontos críticos e dimensionar o sistema corretamente. Sem soluções genéricas."
        },
        {
          "titulo": "Câmeras HD com visão noturna",
          "descricao": "Imagens nítidas durante o dia e a noite, com câmeras coloridas noturnas e infravermelho de longo alcance."
        },
        {
          "titulo": "Acesso remoto pelo celular",
          "descricao": "Acompanhe ao vivo ou revise gravações de qualquer lugar, a qualquer hora, direto no seu smartphone."
        },
        {
          "titulo": "Suporte técnico 24h",
          "descricao": "Equipe de manutenção disponível a noite toda. Se algo parar de funcionar, chamamos você — não o contrário."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Monitore a entrada e o perímetro remotamente", "Identifique visitantes antes de abrir o portão", "Imagens gravadas disponíveis em caso de incidente"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Reduza furtos internos e externos com câmeras visíveis", "Monitore a operação de qualquer filial remotamente", "Evidência em imagem para seguradoras e polícia"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Cobertura completa de áreas comuns, garagem e acessos", "Imagens disponíveis para síndico e conselho", "Integração com portaria e controle de acesso"]
        }
      ],
      "faqs": [
        {
          "pergunta": "Quantas câmeras eu preciso para a minha casa?",
          "resposta": "Depende do tamanho e da planta da residência. Em casas típicas, de 4 a 8 câmeras cobrem a entrada principal, portão, perímetro e garagem. Fazemos um diagnóstico gratuito para dimensionar o projeto corretamente."
        },
        {
          "pergunta": "Por quanto tempo as imagens ficam gravadas?",
          "resposta": "Com um HD de 1TB, um sistema de 4 câmeras Full HD grava entre 15 e 30 dias em loop. Para guardar mais tempo ou ter backup extra, oferecemos armazenamento em nuvem."
        },
        {
          "pergunta": "É possível ver as câmeras pelo celular?",
          "resposta": "Sim. Todos os sistemas que instalamos têm acesso remoto via app (iOS e Android). Você acompanha ao vivo e revisa gravações de qualquer lugar com internet."
        },
        {
          "pergunta": "As câmeras funcionam à noite?",
          "resposta": "Sim. Instalamos câmeras com infravermelho ou visão colorida noturna, que captam imagens nítidas mesmo em ambientes sem iluminação artificial."
        },
        {
          "pergunta": "Qual a diferença entre câmera analógica e IP?",
          "resposta": "Câmeras IP transmitem via rede e oferecem maior resolução, enquanto as analógicas usam cabo coaxial. Para novos projetos recomendamos IP; para ampliação de sistemas existentes, adaptamos ao que já está instalado."
        }
      ]
    },
    {
      "titulo": "Alarme Monitorado 24h",
      "slug": "alarme-monitorado",
      "meta_title": "Alarme Monitorado 24h no Rio de Janeiro | AlarmeForte",
      "meta_description": "Alarme monitorado com central própria 24 horas para residências, empresas e condomínios no Rio de Janeiro. Resposta imediata a qualquer acionamento. Orçamento gratuito.",
      "hero_subtitulo": "Central de monitoramento própria, ativa 24 horas — com resposta imediata a qualquer acionamento no Rio de Janeiro.",
      "descricao": [
        "O alarme monitorado vai além do alarme tradicional: quando acionado, nossa central de monitoramento é notificada imediatamente e toma as providências necessárias — desde contato com o responsável até acionamento das autoridades.",
        "A AlarmeForte opera com central de monitoramento própria, não terceirizada. Isso significa equipe treinada que conhece cada cliente, tempo de resposta reduzido e comunicação direta — sem intermediários.",
        "Instalamos sensores de presença, abertura de portas e janelas, detectores de fumaça e botões de pânico — integrados a um painel inteligente que você controla pelo app ou pelo teclado."
      ],
      "diferenciais": [
        {
          "titulo": "Central própria, não terceirizada",
          "descricao": "Nossa equipe de monitoramento conhece seu endereço, seus contatos e seu histórico. Resposta mais rápida, comunicação direta."
        },
        {
          "titulo": "Resposta em minutos no RJ",
          "descricao": "Equipe técnica de plantão 24h no Rio de Janeiro para atendimentos emergenciais quando necessário."
        },
        {
          "titulo": "Controle pelo app",
          "descricao": "Arme e desarme o sistema remotamente, receba notificações em tempo real e consulte o histórico de acionamentos pelo celular."
        },
        {
          "titulo": "Integração com CFTV",
          "descricao": "O alarme pode ser integrado ao sistema de câmeras: ao ser acionado, a central visualiza as câmeras do local imediatamente."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Proteção total da residência mesmo quando vazia", "Notificação imediata no celular a qualquer acionamento", "Botão do pânico para emergências dentro de casa"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Proteção fora do horário comercial e fins de semana", "Histórico de acionamentos para auditoria", "Integração com câmeras e controle de acesso"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Proteção de áreas comuns, salão de festas e garagem", "Central notifica síndico e portaria simultaneamente", "Sistema escalável para condomínios de qualquer porte"]
        }
      ],
      "faqs": [
        {
          "pergunta": "O que acontece quando o alarme dispara?",
          "resposta": "Nossa central recebe o alerta em segundos. Um operador tenta contato com o responsável cadastrado. Se não houver resposta ou se confirmado o incidente, acionamos a polícia ou equipe de intervenção conforme o plano contratado."
        },
        {
          "pergunta": "O sistema funciona sem internet ou energia elétrica?",
          "resposta": "Sim. O painel tem bateria de backup que mantém o sistema funcionando por horas sem energia. A comunicação com a central usa linha telefônica ou chip GSM como alternativa à internet."
        },
        {
          "pergunta": "Posso armar e desarmar pelo celular?",
          "resposta": "Sim. O app permite controle total do sistema remotamente, além de receber notificações a cada acionamento e consultar o histórico de eventos."
        },
        {
          "pergunta": "Qual o prazo de fidelidade do monitoramento?",
          "resposta": "Trabalhamos com contratos anuais renováveis. Os valores variam conforme o porte do sistema. Entre em contato para um orçamento personalizado."
        },
        {
          "pergunta": "Posso instalar em apartamento?",
          "resposta": "Sim. Temos soluções específicas para apartamentos, com sensores discretos e sem necessidade de obra. A instalação é feita por nossa equipe técnica com o mínimo de interferência."
        }
      ]
    },
    {
      "titulo": "Portaria Inteligente",
      "slug": "portaria-inteligente",
      "meta_title": "Portaria Inteligente para Condomínios no Rio de Janeiro | AlarmeForte",
      "meta_description": "Portaria inteligente e virtual para condomínios no Rio de Janeiro. Reduza até 60% dos custos com porteiro tradicional. Controle remoto, câmeras e interfonia 24h. Orçamento gratuito.",
      "hero_subtitulo": "Gerencie o acesso ao seu condomínio remotamente — com redução de até 60% em relação à portaria tradicional.",
      "descricao": [
        "A portaria inteligente substitui o porteiro presencial por uma central de atendimento remoto que opera 24 horas, 7 dias por semana. Câmeras, interfonia e controle de acesso são integrados em um único sistema gerenciado à distância.",
        "Para condomínios no Rio de Janeiro, a redução de custos é significativa: sem encargos trabalhistas, férias, 13º salário e rotatividade. O investimento no sistema geralmente se paga em menos de 12 meses comparado ao custo do porteiro tradicional.",
        "Moradores autorizam a entrada de visitantes pelo app ou pelo interfone do apartamento. O síndico acessa relatórios de acesso em tempo real e configura as permissões sem precisar de chamado técnico."
      ],
      "diferenciais": [
        {
          "titulo": "Redução de até 60% nos custos",
          "descricao": "Sem encargos trabalhistas, férias ou rotatividade. O sistema se paga em menos de 12 meses para a maioria dos condomínios."
        },
        {
          "titulo": "Atendimento humano 24h",
          "descricao": "Nossa central de portaria remota atende visitantes, entregadores e emergências com operadores treinados, 24 horas por dia."
        },
        {
          "titulo": "App para moradores e síndico",
          "descricao": "Moradores autorizam visitas pelo celular. O síndico acessa relatórios, configura acessos e recebe alertas em tempo real."
        },
        {
          "titulo": "Integração total de sistemas",
          "descricao": "Câmeras, interfonia digital, cancelas e controle de acesso em um único sistema integrado — sem gambiarras ou adaptações."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Autorize visitantes pelo celular de qualquer lugar", "Histórico completo de entradas e saídas", "Redução de custo sem abrir mão da segurança"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Controle de acesso por horário e perfil de colaborador", "Relatórios de presença integrados ao RH", "Acesso remoto para gestão de múltiplas unidades"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Redução imediata de custos operacionais", "Eliminação de problemas com porteiros (falta, postura, turnover)", "Cobertura 24h com qualidade uniforme e auditável"]
        }
      ],
      "faqs": [
        {
          "pergunta": "O que acontece em caso de emergência sem porteiro físico?",
          "resposta": "Nossa central atende 24 horas e aciona os protocolos de emergência — desde contato com moradores até acionamento de serviços de emergência. O sistema também integra com alarmes e câmeras para visão imediata da situação."
        },
        {
          "pergunta": "É possível ter porteiro físico e portaria remota ao mesmo tempo?",
          "resposta": "Sim. Muitos condomínios adotam o modelo híbrido: porteiro físico no horário comercial e portaria remota à noite e fins de semana, reduzindo o custo sem eliminar a presença humana."
        },
        {
          "pergunta": "Como funciona a autorização de entregadores?",
          "resposta": "O operador da central identifica o entregador, comunica ao morador via app ou interfone, e libera ou nega o acesso conforme a resposta. O morador também pode configurar autorizações prévias para prestadores frequentes."
        },
        {
          "pergunta": "Meu condomínio antigo pode adotar portaria inteligente?",
          "resposta": "Na maioria dos casos sim. Fazemos uma vistoria técnica gratuita para avaliar a infraestrutura existente e propor a melhor solução, aproveitando o cabeamento e equipamentos já instalados quando possível."
        }
      ]
    },
    {
      "titulo": "Interfonia Condominial",
      "slug": "interfonia",
      "meta_title": "Interfonia Condominial no Rio de Janeiro | AlarmeForte",
      "meta_description": "Instalação e manutenção de interfonia condominial no Rio de Janeiro. Sistemas analógicos e digitais, todas as marcas. Mais de 30 anos de experiência. Orçamento gratuito.",
      "hero_subtitulo": "Sistemas de interfonia analógicos e digitais para condomínios — instalação profissional e manutenção especializada no Rio de Janeiro.",
      "descricao": [
        "O sistema de interfonia é o primeiro ponto de contato entre visitantes e moradores de um condomínio. Um sistema bem instalado e mantido garante comunicação clara, controle de acesso eficiente e longevidade do equipamento.",
        "A AlarmeForte instala e mantém sistemas de interfonia analógicos e digitais das principais marcas do mercado — Intelbras, HDL, Comelit, AGL e outras. Atendemos condomínios residenciais e comerciais de qualquer porte, desde prédios com 4 unidades até grandes torres.",
        "Além da instalação de novos sistemas, realizamos modernizações de infraestrutura existente, substituição de componentes defeituosos e manutenção preventiva — tudo com peças originais e garantia de serviço."
      ],
      "diferenciais": [
        {
          "titulo": "Todas as marcas e tecnologias",
          "descricao": "Trabalhamos com sistemas analógicos tradicionais, vídeo porteiro colorido, interfonia IP e integração com apps de acesso remoto."
        },
        {
          "titulo": "Manutenção preventiva",
          "descricao": "Programa de manutenção periódica que identifica problemas antes que causem falhas — sem surpresas para o condomínio."
        },
        {
          "titulo": "Peças originais com garantia",
          "descricao": "Usamos apenas peças originais dos fabricantes, com nota fiscal e garantia. Sem gambiarras que comprometem a segurança."
        },
        {
          "titulo": "Atendimento rápido no RJ",
          "descricao": "Equipe técnica baseada no Rio de Janeiro com tempo de resposta para emergências. Falha na interfonia é urgência — tratamos assim."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Comunicação clara com visitantes antes de abrir o portão", "Vídeo porteiro com câmera para identificação visual", "Integração com fechadura elétrica ou cancela"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Controle de acesso para funcionários e visitantes", "Ramais para diferentes departamentos ou andares", "Registro de chamadas e acessos"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Sistema completo com ramal em cada unidade", "Interfone na portaria e nas áreas comuns", "Compatível com portaria inteligente e controle de acesso"]
        }
      ],
      "faqs": [
        {
          "pergunta": "Qual a diferença entre interfonia analógica e digital?",
          "resposta": "A analógica usa cabeamento dedicado para cada ramal (cabo par trançado), é mais simples e robusta para condomínios já cabeados. A digital (ou IP) transmite voz e vídeo via rede estruturada, oferece mais recursos e facilidade de expansão, mas exige infraestrutura de rede adequada."
        },
        {
          "pergunta": "Precisamos trocar todo o sistema para modernizar?",
          "resposta": "Não necessariamente. Em muitos casos é possível substituir apenas a central e os terminais externos, aproveitando o cabeamento existente. Fazemos uma vistoria gratuita para avaliar o que pode ser reaproveitado."
        },
        {
          "pergunta": "E em prédios antigos com cabeamento deteriorado?",
          "resposta": "Temos experiência com retrofit completo em prédios antigos — substituição de cabeamento, modernização dos ramais e instalação de nova central. O projeto é feito para causar o mínimo de transtorno aos moradores."
        },
        {
          "pergunta": "É possível adicionar câmera ao sistema de interfonia existente?",
          "resposta": "Depende do sistema atual. Sistemas mais modernos suportam a adição de vídeo. Para sistemas mais antigos, geralmente fazemos a substituição da unidade externa por um modelo com câmera integrada."
        }
      ]
    },
    {
      "titulo": "Controle de Acesso Facial",
      "slug": "controle-acesso",
      "meta_title": "Controle de Acesso Facial no Rio de Janeiro | AlarmeForte",
      "meta_description": "Controle de acesso por biometria facial para residências, empresas e condomínios no Rio de Janeiro. Sem chaves, sem cartões, máxima segurança. Orçamento gratuito.",
      "hero_subtitulo": "Biometria facial para controle de acesso — sem chaves, sem cartões, sem falhas humanas.",
      "descricao": [
        "O controle de acesso facial elimina chaves, cartões e senhas — substituindo tudo pela característica mais única e intransferível de cada pessoa: o rosto. A tecnologia de reconhecimento facial de última geração garante precisão de 99,9% e resposta em menos de 0,5 segundo.",
        "Para empresas e condomínios, o benefício vai além da segurança: há um registro completo de quem entrou e saiu, em qual horário, e por qual porta. Esse histórico é acessível em tempo real pelo app ou pelo painel de gestão.",
        "A AlarmeForte instala e configura sistemas de controle de acesso facial integrados ao sistema de alarme e CFTV existente — ou como solução autônoma, sem necessidade de reformas."
      ],
      "diferenciais": [
        {
          "titulo": "Sem chaves nem cartões",
          "descricao": "Chaves se perdem, cartões são clonados. O rosto é a credencial mais segura e impossível de esquecer ou transferir."
        },
        {
          "titulo": "Registro completo de acesso",
          "descricao": "Cada entrada e saída é registrada com foto, horário e identificação do usuário — disponível em tempo real no app ou no painel."
        },
        {
          "titulo": "Integração com câmeras e alarme",
          "descricao": "O sistema se integra com CFTV e alarme: acesso não autorizado gera alerta imediato na central de monitoramento."
        },
        {
          "titulo": "Cadastro simples e rápido",
          "descricao": "Novos usuários são cadastrados em menos de 1 minuto, sem necessidade de técnico no local. Remoção de acesso é instantânea."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Acesso sem chave para todos os moradores", "Histórico de entradas disponível para o proprietário", "Autorização temporária para prestadores de serviço"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Controle de acesso por horário e área para cada colaborador", "Relatório de presença integrado", "Bloqueio imediato em caso de demissão, sem recolher crachá"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Acesso exclusivo para moradores e autorizados", "Registro completo disponível para o síndico", "Integração com portaria inteligente e interfonia"]
        }
      ],
      "faqs": [
        {
          "pergunta": "O sistema funciona com óculos ou máscara?",
          "resposta": "Sim. Os equipamentos que instalamos usam tecnologia de reconhecimento 3D que funciona com óculos, chapéu e variações no visual. Para máscaras, o sistema pode ser configurado para aceitar reconhecimento parcial ou exigir complemento por PIN."
        },
        {
          "pergunta": "O que acontece em caso de falta de energia?",
          "resposta": "O sistema tem bateria de backup e pode ser configurado para liberar ou bloquear o acesso automaticamente em caso de queda de energia, conforme a política de segurança do local."
        },
        {
          "pergunta": "É possível usar foto para enganar o sistema?",
          "resposta": "Não. Os equipamentos que instalamos usam detecção de vivacidade (liveness detection), que diferencia um rosto real de uma foto ou tela. Tentativas de fraude são registradas e geram alerta."
        },
        {
          "pergunta": "Como funciona o cadastro de novos usuários?",
          "resposta": "O administrador (síndico, gerente ou proprietário) faz o cadastro diretamente no painel web ou no app, sem necessidade de presença do técnico. O novo usuário fica com acesso liberado imediatamente após o cadastro."
        }
      ]
    },
    {
      "titulo": "Monitoramento Remoto",
      "slug": "monitoramento-remoto",
      "meta_title": "Monitoramento Remoto de Câmeras no Rio de Janeiro | AlarmeForte",
      "meta_description": "Monitoramento remoto de câmeras com backup em nuvem para residências e empresas no Rio de Janeiro. Acesse de qualquer lugar, a qualquer hora. Orçamento gratuito.",
      "hero_subtitulo": "Acesse suas câmeras de qualquer lugar e tenha as imagens protegidas em nuvem — 24 horas, 7 dias por semana.",
      "descricao": [
        "O monitoramento remoto permite que você acompanhe ao vivo o que acontece no seu patrimônio de qualquer lugar do mundo, a qualquer hora. Seja pelo celular, tablet ou computador — com a mesma qualidade de imagem do gravador local.",
        "O backup em nuvem resolve o ponto vulnerável dos sistemas tradicionais: se o DVR for roubado ou danificado, as imagens gravadas na nuvem ficam intactas e acessíveis. O armazenamento é criptografado e seguro.",
        "A AlarmeForte configura o acesso remoto em todos os sistemas que instala, e oferece planos de armazenamento em nuvem adaptados a cada necessidade — de 7 dias a 90 dias de histórico."
      ],
      "diferenciais": [
        {
          "titulo": "Backup em nuvem criptografado",
          "descricao": "Imagens gravadas na nuvem mesmo que o equipamento local seja danificado ou roubado. Acesso exclusivo por senha segura."
        },
        {
          "titulo": "Acesso de múltiplos dispositivos",
          "descricao": "Até 5 usuários com diferentes níveis de permissão podem acessar as câmeras simultaneamente — família, sócios, equipe de segurança."
        },
        {
          "titulo": "Alertas em tempo real",
          "descricao": "Notificações push no celular quando há detecção de movimento em zonas configuradas — você é avisado antes de precisar checar."
        },
        {
          "titulo": "Planos de armazenamento flexíveis",
          "descricao": "De 7 a 90 dias de histórico na nuvem, com opção de download de clipes específicos para uso como prova ou registro."
        }
      ],
      "perfis": [
        {
          "tipo": "Residencial",
          "beneficios": ["Acompanhe sua casa remotamente em viagens", "Receba alertas de movimento em áreas sensíveis", "Histórico disponível para conferir incidentes passados"]
        },
        {
          "tipo": "Comercial",
          "beneficios": ["Monitore filiais e depósitos de qualquer lugar", "Compartilhe acesso com sócios ou gerentes por unidade", "Evidência em nuvem para seguradoras em caso de sinistro"]
        },
        {
          "tipo": "Condominial",
          "beneficios": ["Síndico e conselho acessam câmeras pelo app", "Histórico preservado mesmo em caso de vandalismo ao DVR", "Relatório de eventos exportável para assembleias"]
        }
      ],
      "faqs": [
        {
          "pergunta": "Precisa de internet rápida para funcionar?",
          "resposta": "Para acesso remoto em qualidade Full HD, recomendamos pelo menos 10 Mbps de upload no local das câmeras. Para visualização no celular, 4G já é suficiente. O sistema também funciona em redes mais lentas, com qualidade de imagem adaptada automaticamente."
        },
        {
          "pergunta": "As imagens na nuvem são seguras?",
          "resposta": "Sim. O armazenamento usa criptografia AES-256 e acesso exclusivo por credenciais do proprietário. Nem a AlarmeForte acessa suas imagens sem sua autorização."
        },
        {
          "pergunta": "Posso compartilhar acesso com outras pessoas?",
          "resposta": "Sim. O sistema permite cadastrar múltiplos usuários com diferentes permissões — por exemplo, um usuário que só vê câmeras externas, ou outro que tem acesso a todas as câmeras mas não pode configurar o sistema."
        },
        {
          "pergunta": "O que acontece quando acaba o plano de armazenamento?",
          "resposta": "O sistema sobrescreve automaticamente as imagens mais antigas (gravar em loop), ou envia um aviso para renovação, dependendo da configuração escolhida. Você nunca perde imagens recentes por falta de espaço sem ser avisado."
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add data/servicos.json
git commit -m "data: add servicos.json with full content for 6 service pages"
```

---

## Task 4: data/posts.json

**Files:**
- Criar: `data/posts.json`

- [ ] **Step 1: Criar data/posts.json com schema inicial vazio**

```json
{
  "posts": []
}
```

- [ ] **Step 2: Commit**

```bash
git add data/posts.json
git commit -m "data: add posts.json empty schema"
```

---

## Task 5: templates/base.html

**Files:**
- Criar: `templates/base.html`

Este template contém nav e footer que todas as páginas compartilham. Usa variáveis `site` (de site.json) e `servicos` (de servicos.json) injetadas pelo build.py.

- [ ] **Step 1: Criar templates/base.html**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{% block meta_description %}AlarmeForte — 30 anos de segurança eletrônica no Rio de Janeiro. Câmeras CFTV, alarmes monitorados, portaria inteligente e controle de acesso.{% endblock %}">
  <meta property="og:title" content="{% block og_title %}AlarmeForte | Segurança Eletrônica no Rio de Janeiro{% endblock %}">
  <meta property="og:description" content="{% block og_description %}30 anos protegendo residências, empresas e condomínios no Rio de Janeiro.{% endblock %}">
  <meta property="og:type" content="website">
  <meta name="author" content="AlarmeForte">
  <title>{% block title %}AlarmeForte | Segurança Eletrônica no Rio de Janeiro{% endblock %}</title>
  {% block extra_head %}{% endblock %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

  <!-- ===== NAVIGATION ===== -->
  <nav id="navbar" class="navbar">
    <div class="nav-container">
      <a href="/" class="nav-logo">
        <img src="/img/logo.png" alt="AlarmeForte" class="logo-img">
      </a>
      <ul class="nav-links" id="navLinks">
        <li class="nav-dropdown-wrapper">
          <a href="#" class="nav-dropdown-toggle" aria-haspopup="true" aria-expanded="false">
            Serviços
            <svg viewBox="0 0 12 8" width="10" height="7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M1 1l5 5 5-5"/></svg>
          </a>
          <div class="nav-dropdown-menu" role="menu">
            {% for s in servicos %}
            <a href="/servicos/{{ s.slug }}/" role="menuitem">{{ s.titulo }}</a>
            {% endfor %}
          </div>
        </li>
        <li><a href="/#sobre">Sobre</a></li>
        <li><a href="/noticias/">Blog</a></li>
        <li><a href="/#contato">Contato</a></li>
      </ul>
      <a href="/#contato" class="btn btn-primary nav-cta">Solicitar Orçamento</a>
      <button class="hamburger" id="hamburger" aria-label="Abrir menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>

  {% block content %}{% endblock %}

  <!-- ===== FOOTER ===== -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="nav-logo footer-logo">
            <img src="/img/logo.png" alt="AlarmeForte" class="logo-img">
          </a>
          <p class="footer-tagline">30 anos protegendo o que importa no Rio de Janeiro. Desde 1992.</p>
        </div>
        <div class="footer-links">
          <h4>Serviços</h4>
          <ul>
            {% for s in servicos %}
            <li><a href="/servicos/{{ s.slug }}/">{{ s.titulo }}</a></li>
            {% endfor %}
          </ul>
        </div>
        <div class="footer-links">
          <h4>Empresa</h4>
          <ul>
            <li><a href="/#sobre">Sobre Nós</a></li>
            <li><a href="/#como-funciona">Como Funciona</a></li>
            <li><a href="/noticias/">Blog</a></li>
            <li><a href="/#contato">Contato</a></li>
            <li><a href="{{ site.politica_privacidade }}" target="_blank" rel="noopener">Política de Privacidade</a></li>
          </ul>
        </div>
        <div class="footer-contact">
          <h4>Contato</h4>
          <p><a href="tel:{{ site.telefone_link }}">{{ site.telefone }}</a></p>
          <p>{{ site.cidade }}</p>
          <p class="footer-hours">Atendimento 24 horas</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2025 AlarmeForte. Todos os direitos reservados.</p>
        <p>Segurança Eletrônica no Rio de Janeiro desde {{ site.ano_fundacao }}.</p>
      </div>
    </div>
  </footer>

  <!-- WhatsApp Floating Button -->
  <a href="https://wa.me/{{ site.whatsapp }}?text={{ site.whatsapp_mensagem | urlencode }}"
     class="whatsapp-btn"
     target="_blank"
     rel="noopener noreferrer"
     aria-label="Fale conosco pelo WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28" aria-hidden="true">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>
    <span class="whatsapp-label">Fale no WhatsApp</span>
  </a>

  <script src="/js/main.js"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add templates/base.html
git commit -m "feat: add base.html template with nav dropdown and footer"
```

---

## Task 6: build.py

**Files:**
- Criar: `build.py`

- [ ] **Step 1: Criar build.py**

```python
"""
build.py — AlarmeForte V2
Gera todo o HTML estático a partir de data/*.json + templates/*.html
Uso: python build.py
"""
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
from datetime import date

ROOT = Path(__file__).parent


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def render(env: Environment, template_name: str, output_path: Path, context: dict) -> None:
    template = env.get_template(template_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.render(**context), encoding='utf-8')
    print(f'  ✓ {output_path.relative_to(ROOT)}')


def generate_sitemap(root: Path, servicos: list, posts: list, site: dict) -> None:
    base = site['url'].rstrip('/')
    urls = [
        f'{base}/',
        f'{base}/noticias/',
    ]
    for s in servicos:
        urls.append(f"{base}/servicos/{s['slug']}/")
    for p in posts:
        urls.append(f"{base}/noticias/{p['slug']}/")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.append(f'  <url><loc>{url}</loc></url>')
    lines.append('</urlset>')

    (root / 'sitemap.xml').write_text('\n'.join(lines), encoding='utf-8')
    print('  ✓ sitemap.xml')


def generate_robots(root: Path, site: dict) -> None:
    content = f"User-agent: *\nAllow: /\nSitemap: {site['url'].rstrip('/')}/sitemap.xml\n"
    (root / 'robots.txt').write_text(content, encoding='utf-8')
    print('  ✓ robots.txt')


def build() -> None:
    env = Environment(
        loader=FileSystemLoader(ROOT / 'templates'),
        autoescape=True
    )

    site = load_json('data/site.json')
    servicos = load_json('data/servicos.json')['servicos']
    all_posts = load_json('data/posts.json')['posts']
    posts = [p for p in all_posts if p.get('status') == 'publicado']

    ctx_base = {'site': site, 'servicos': servicos}

    print('\nBuilding AlarmeForte V2...')

    # Homepage
    render(env, 'homepage.html', ROOT / 'index.html',
           {**ctx_base, 'posts_recentes': posts[:3]})

    # Service pages
    for servico in servicos:
        output = ROOT / 'servicos' / servico['slug'] / 'index.html'
        render(env, 'servico.html', output, {**ctx_base, 'servico': servico})

    # Blog index
    render(env, 'blog-index.html', ROOT / 'noticias' / 'index.html',
           {**ctx_base, 'posts': posts})

    # Individual posts
    for post in posts:
        output = ROOT / 'noticias' / post['slug'] / 'index.html'
        render(env, 'post.html', output, {**ctx_base, 'post': post})

    # SEO files
    generate_sitemap(ROOT, servicos, posts, site)
    generate_robots(ROOT, site)

    total = 1 + len(servicos) + 1 + len(posts)
    print(f'\n✅ Build completo — {total} páginas geradas\n')


if __name__ == '__main__':
    build()
```

- [ ] **Step 2: Commit**

```bash
git add build.py
git commit -m "feat: add build.py Jinja2 static site generator"
```

---

## Task 7: templates/homepage.html

**Files:**
- Criar: `templates/homepage.html`

Refatora o `index.html` atual para usar base.html. O conteúdo das seções (hero, serviços, sobre, stats, como funciona, contato) é mantido idêntico — apenas os links de serviço são atualizados para apontar para as páginas dedicadas.

- [ ] **Step 1: Criar templates/homepage.html**

```html
{% extends 'base.html' %}

{% block title %}AlarmeForte | Segurança Eletrônica no Rio de Janeiro{% endblock %}
{% block meta_description %}AlarmeForte — 30 anos de segurança eletrônica no Rio de Janeiro. Câmeras CFTV, alarmes monitorados, portaria inteligente e controle de acesso para residências, empresas e condomínios.{% endblock %}

{% block content %}

  <!-- ===== HERO ===== -->
  <section id="hero" class="hero">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="container hero-content">
      <div class="hero-badge reveal">
        <svg viewBox="0 0 8 8" width="8" height="8" aria-hidden="true"><circle cx="4" cy="4" r="4" fill="#84C25B"/></svg>
        30 Anos Protegendo o Rio de Janeiro
      </div>
      <h1 class="hero-title reveal reveal-delay-1">
        Segurança que o Rio<br>
        de Janeiro confia<br>
        <em>há 30 anos.</em>
      </h1>
      <p class="hero-subtitle reveal reveal-delay-2">
        Câmeras CFTV, alarmes monitorados, portaria inteligente e controle de acesso
        para residências, empresas e condomínios.
      </p>
      <div class="hero-actions reveal reveal-delay-3">
        <a href="/#contato" class="btn btn-primary btn-lg">Solicitar Orçamento</a>
        <a href="#servicos" class="btn btn-outline btn-lg">Ver Serviços</a>
      </div>
      <div class="hero-trust reveal reveal-delay-4">
        <span>
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.18 2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke-linecap="round" stroke-linejoin="round"/></svg>
          {{ site.telefone }}
        </span>
        <span class="trust-sep" aria-hidden="true">·</span>
        <span>Atendimento 24h</span>
        <span class="trust-sep" aria-hidden="true">·</span>
        <span>{{ site.cidade }}</span>
      </div>
    </div>
    <div class="hero-scroll-indicator" aria-hidden="true">
      <div class="scroll-line"></div>
    </div>
  </section>

  <!-- ===== SERVIÇOS ===== -->
  <section id="servicos" class="section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Nossos Serviços</span>
        <h2 class="section-title">Soluções completas de<br>segurança eletrônica</h2>
        <p class="section-subtitle">Projetos customizados para cada necessidade — residencial, comercial ou condominial.</p>
      </div>
      <div class="services-grid">

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="8" width="13" height="8" rx="1"/>
              <path d="M15 11l4.55-2.28A1 1 0 0121 9.57V14.4a1 1 0 01-1.45.9L15 13"/>
              <circle cx="8" cy="12" r="1.5"/>
            </svg>
          </div>
          <h3>Sistema de CFTV</h3>
          <p>Câmeras HD para monitoramento de residências, empresas e condomínios, com acesso remoto via celular.</p>
          <a href="/servicos/cftv/" class="service-link">Saiba mais →</a>
        </article>

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2C8.13 2 5 5.13 5 9v4l-2 2v1h18v-1l-2-2V9c0-3.87-3.13-7-7-7zm0 20c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2z"/>
            </svg>
          </div>
          <h3>Alarme Monitorado 24h</h3>
          <p>Central de monitoramento ativa 24 horas com resposta de emergência imediata para sua segurança.</p>
          <a href="/servicos/alarme-monitorado/" class="service-link">Saiba mais →</a>
        </article>

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M9 3v18M15 9h1M15 12h1M15 15h1"/>
            </svg>
          </div>
          <h3>Portaria Inteligente</h3>
          <p>Gerencie o acesso ao seu condomínio remotamente. Redução de até <strong>60% nos custos</strong> em relação à portaria tradicional.</p>
          <a href="/servicos/portaria-inteligente/" class="service-link">Saiba mais →</a>
        </article>

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.18 2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
            </svg>
          </div>
          <h3>Interfonia Condominial</h3>
          <p>Sistemas analógicos e digitais de interfonia para condomínios — instalação completa e manutenção especializada.</p>
          <a href="/servicos/interfonia/" class="service-link">Saiba mais →</a>
        </article>

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2a10 10 0 100 20 10 10 0 000-20z"/>
              <path d="M12 8v4l3 3"/>
            </svg>
          </div>
          <h3>Controle de Acesso Facial</h3>
          <p>Biometria facial para controle de acesso seguro — sem chaves, sem cartões, sem falhas humanas.</p>
          <a href="/servicos/controle-acesso/" class="service-link">Saiba mais →</a>
        </article>

        <article class="service-card reveal">
          <div class="service-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/>
            </svg>
          </div>
          <h3>Monitoramento Remoto</h3>
          <p>Backup de imagens na nuvem e monitoramento remoto — acesse suas câmeras de qualquer lugar, a qualquer hora.</p>
          <a href="/servicos/monitoramento-remoto/" class="service-link">Saiba mais →</a>
        </article>

      </div>
    </div>
  </section>

  <!-- ===== POR QUE ALARMEFORTE ===== -->
  <section id="sobre" class="section-dark">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Por que a AlarmeForte?</span>
        <h2 class="section-title section-title-light">30 anos é uma história.<br><em>Segurança é nossa tradição.</em></h2>
      </div>
      <div class="features-grid">
        <div class="feature-card reveal">
          <div class="feature-number" aria-hidden="true">01</div>
          <h3>30 Anos no Mercado</h3>
          <p>Desde 1992 no Rio de Janeiro. Gerações de clientes que confiam na AlarmeForte para proteger o que é mais importante.</p>
        </div>
        <div class="feature-card reveal">
          <div class="feature-number" aria-hidden="true">02</div>
          <h3>Projetos Sob Medida</h3>
          <p>Não existe solução genérica. Cada projeto é desenvolvido para a realidade específica do cliente — residência, empresa ou condomínio.</p>
        </div>
        <div class="feature-card reveal">
          <div class="feature-number" aria-hidden="true">03</div>
          <h3>Atendimento 24 Horas</h3>
          <p>Central de monitoramento ativa a noite toda. Em caso de emergência, nossa equipe responde 24h por dia, 7 dias por semana.</p>
        </div>
        <div class="feature-card reveal">
          <div class="feature-number" aria-hidden="true">04</div>
          <h3>Especialistas no Rio</h3>
          <p>Conhecemos a realidade da segurança carioca. Equipe técnica experiente, treinada para as especificidades da cidade.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== NÚMEROS ===== -->
  <section id="numeros" class="section-stats">
    <div class="container">
      <div class="stats-grid">
        <div class="stat-item reveal">
          <div class="stat-value">
            <span class="stat-number" data-target="30">0</span><span class="stat-suffix">+</span>
          </div>
          <span class="stat-label">Anos de Experiência</span>
        </div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat-item reveal">
          <div class="stat-value">
            <span class="stat-number" data-target="1500">0</span><span class="stat-suffix">+</span>
          </div>
          <span class="stat-label">Clientes Atendidos</span>
        </div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat-item reveal">
          <div class="stat-value">
            <span class="stat-number" data-target="8000">0</span><span class="stat-suffix">+</span>
          </div>
          <span class="stat-label">Projetos Realizados</span>
        </div>
        <div class="stat-divider" aria-hidden="true"></div>
        <div class="stat-item reveal">
          <div class="stat-value">
            <span class="stat-number">24</span><span class="stat-suffix">h</span>
          </div>
          <span class="stat-label">Suporte Contínuo</span>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== COMO FUNCIONA ===== -->
  <section id="como-funciona" class="section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Como Funciona</span>
        <h2 class="section-title">Do diagnóstico à proteção<br>em 3 passos</h2>
      </div>
      <div class="steps-grid">
        <div class="step reveal">
          <div class="step-number" aria-hidden="true">01</div>
          <h3>Diagnóstico Gratuito</h3>
          <p>Nossa equipe visita o local, identifica as vulnerabilidades e entende as necessidades específicas de segurança — sem custo.</p>
        </div>
        <div class="step-connector" aria-hidden="true">
          <svg viewBox="0 0 40 16" fill="none"><path d="M0 8h36M30 2l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <div class="step reveal">
          <div class="step-number" aria-hidden="true">02</div>
          <h3>Projeto e Instalação</h3>
          <p>Desenvolvemos um projeto customizado e realizamos a instalação profissional com equipamentos de qualidade comprovada.</p>
        </div>
        <div class="step-connector" aria-hidden="true">
          <svg viewBox="0 0 40 16" fill="none"><path d="M0 8h36M30 2l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <div class="step reveal">
          <div class="step-number" aria-hidden="true">03</div>
          <h3>Monitoramento Contínuo</h3>
          <p>Ativamos o monitoramento 24h e oferecemos suporte técnico permanente para manter sua segurança sempre ativa.</p>
        </div>
      </div>
      <div class="steps-cta reveal">
        <a href="/#contato" class="btn btn-primary btn-lg">Agendar Diagnóstico Gratuito</a>
      </div>
    </div>
  </section>

  <!-- ===== CONTATO ===== -->
  <section id="contato" class="section-dark">
    <div class="container">
      <div class="contact-grid">
        <div class="contact-info reveal">
          <span class="section-label">Fale Conosco</span>
          <h2 class="section-title section-title-light">Fale com nossos<br><em>especialistas</em></h2>
          <p class="contact-subtitle">Resposta em até 30 minutos durante horário comercial. Diagnóstico gratuito, sem compromisso.</p>
          <div class="contact-details">
            <a href="tel:{{ site.telefone_link }}" class="contact-item">
              <div class="contact-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
                  <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.18 2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
                </svg>
              </div>
              <div>
                <span class="contact-label">Telefone</span>
                <span class="contact-value">{{ site.telefone }}</span>
              </div>
            </a>
            <div class="contact-item">
              <div class="contact-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" width="18" height="18">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div>
                <span class="contact-label">Atendimento</span>
                <span class="contact-value">24 horas, 7 dias por semana</span>
              </div>
            </div>
            <div class="contact-item">
              <div class="contact-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </div>
              <div>
                <span class="contact-label">Localização</span>
                <span class="contact-value">{{ site.cidade }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="contact-form-wrapper reveal">
          <form id="contactForm" class="contact-form" action="https://formspree.io/f/YOUR_FORMSPREE_ID" method="POST">
            <div class="form-row">
              <div class="form-group">
                <label for="name">Nome completo</label>
                <input type="text" id="name" name="name" placeholder="Seu nome" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="phone">Telefone / WhatsApp</label>
                <input type="tel" id="phone" name="phone" placeholder="(21) 99999-9999" required autocomplete="tel">
              </div>
            </div>
            <div class="form-group">
              <label for="email">E-mail</label>
              <input type="email" id="email" name="email" placeholder="seu@email.com" required autocomplete="email">
            </div>
            <div class="form-group">
              <label for="service">Serviço de interesse</label>
              <select id="service" name="service">
                <option value="">Selecione um serviço...</option>
                {% for s in servicos %}
                <option>{{ s.titulo }}</option>
                {% endfor %}
                <option>Assistência Técnica</option>
                <option>Outro / Não sei ainda</option>
              </select>
            </div>
            <div class="form-group">
              <label for="message">Mensagem <span class="label-optional">(opcional)</span></label>
              <textarea id="message" name="message" rows="3" placeholder="Descreva brevemente sua necessidade..."></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-full btn-lg" id="submitBtn">
              <span class="btn-text">Solicitar Orçamento Gratuito</span>
              <span class="btn-loading" hidden>Enviando...</span>
            </button>
            <p class="form-note">Sem compromisso. Diagnóstico gratuito.</p>
          </form>
          <div id="formSuccess" class="form-success" hidden>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="56" height="56">
              <path d="M22 11.08V12a10 10 0 11-5.93-9.14" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="22 4 12 14.01 9 11.01" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3>Mensagem recebida!</h3>
            <p>Nossa equipe entrará em contato em até 30 minutos.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

{% endblock %}
```

- [ ] **Step 2: Commit**

```bash
git add templates/homepage.html
git commit -m "feat: add homepage.html extending base template"
```

---

## Task 8: Smoke test — build gera homepage

**Files:**
- Criar: `tests/test_build.py`

- [ ] **Step 1: Escrever tests/test_build.py**

```python
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
```

- [ ] **Step 2: Rodar os testes (vão falhar — templates de serviço e blog ainda não existem)**

```bash
pytest tests/test_build.py -v
```

Saída esperada: `test_build_exits_successfully` FALHA com erro de template não encontrado. Isso é esperado — ainda precisamos criar `servico.html` e `blog-index.html`.

- [ ] **Step 3: Criar templates mínimos temporários para desbloquear o build**

```bash
echo "{% extends 'base.html' %}{% block content %}<h1>{{ servico.titulo }}</h1>{% endblock %}" > templates/servico.html
echo "{% extends 'base.html' %}{% block content %}<h1>Blog</h1>{% endblock %}" > templates/blog-index.html
echo "{% extends 'base.html' %}{% block content %}<h1>{{ post.titulo }}</h1>{% endblock %}" > templates/post.html
```

- [ ] **Step 4: Rodar os testes novamente**

```bash
pytest tests/test_build.py -v
```

Saída esperada: todos os 5 testes PASSAM.

- [ ] **Step 5: Commit**

```bash
git add tests/test_build.py templates/servico.html templates/blog-index.html templates/post.html
git commit -m "test: add build smoke tests; add placeholder templates"
```

---

## Task 9: CSS — novos componentes

**Files:**
- Modificar: `css/style.css` (append ao final)

- [ ] **Step 1: Adicionar componentes CSS ao final de css/style.css**

Abrir `css/style.css` e adicionar ao final:

```css
/* ===========================
   PAGE HERO (páginas internas)
   =========================== */
.page-hero {
  background: var(--dark-bg);
  padding: 128px 0 72px;
  position: relative;
  overflow: hidden;
}
.page-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 55% 80% at 90% 50%, rgba(31, 105, 58, 0.2) 0%, transparent 60%),
    radial-gradient(ellipse 35% 50% at 5% 90%, rgba(132, 194, 91, 0.06) 0%, transparent 55%);
  pointer-events: none;
}
.page-hero-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
}
.page-hero-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4.5vw, 3.4rem);
  font-weight: 600;
  color: var(--text-light);
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -0.01em;
}
.page-hero-subtitle {
  font-size: clamp(0.95rem, 1.8vw, 1.08rem);
  color: var(--text-muted);
  line-height: 1.75;
  margin-bottom: 36px;
  max-width: 580px;
}

/* ===========================
   BREADCRUMB
   =========================== */
.breadcrumb-bar {
  background: var(--dark-bg);
  border-bottom: 1px solid var(--dark-border);
  padding: 0;
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 0;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.breadcrumb a {
  color: var(--text-muted);
  transition: color var(--t);
}
.breadcrumb a:hover { color: var(--green-accent); }
.breadcrumb-sep { opacity: 0.35; }
.breadcrumb-current { color: var(--green-accent); font-weight: 500; }

/* ===========================
   FAQ ACCORDION
   =========================== */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 760px;
  margin: 0 auto;
}
.faq-item {
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  overflow: hidden;
}
.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 22px;
  background: var(--white);
  text-align: left;
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-dark);
  cursor: pointer;
  transition: background var(--t), color var(--t);
  border: none;
}
.faq-question:hover { background: var(--light-bg); }
.faq-question.open { color: var(--green-primary); background: var(--light-bg); }
.faq-answer {
  padding: 0 22px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.32s ease, padding 0.32s ease;
  font-size: 0.875rem;
  color: var(--text-gray);
  line-height: 1.75;
  background: var(--white);
}
.faq-answer.open {
  max-height: 400px;
  padding: 4px 22px 20px;
}
.faq-icon {
  flex-shrink: 0;
  color: var(--green-primary);
  transition: transform var(--t);
}
.faq-question.open .faq-icon { transform: rotate(45deg); }

/* ===========================
   NAV DROPDOWN
   =========================== */
.nav-dropdown-wrapper {
  position: relative;
}
.nav-dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 5px;
  color: rgba(240, 245, 241, 0.65);
  font-size: 0.86rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  transition: color var(--t);
  cursor: pointer;
}
.nav-dropdown-toggle:hover,
.nav-dropdown-wrapper.open .nav-dropdown-toggle { color: var(--text-light); }
.nav-dropdown-toggle svg { transition: transform var(--t); }
.nav-dropdown-wrapper.open .nav-dropdown-toggle svg { transform: rotate(180deg); }

.nav-dropdown-menu {
  position: absolute;
  top: calc(100% + 14px);
  left: -16px;
  background: rgba(8, 14, 9, 0.97);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--dark-border);
  border-radius: var(--radius-lg);
  padding: 8px;
  min-width: 230px;
  opacity: 0;
  pointer-events: none;
  transform: translateY(-6px);
  transition: opacity var(--t), transform var(--t);
  z-index: 200;
}
.nav-dropdown-wrapper.open .nav-dropdown-menu {
  opacity: 1;
  pointer-events: all;
  transform: translateY(0);
}
.nav-dropdown-menu a {
  display: block;
  padding: 9px 14px;
  border-radius: var(--radius);
  font-size: 0.84rem;
  color: rgba(240, 245, 241, 0.65);
  transition: background var(--t), color var(--t);
  letter-spacing: 0;
}
.nav-dropdown-menu a:hover {
  background: rgba(31, 105, 58, 0.15);
  color: var(--text-light);
}
.nav-dropdown-menu a::after { display: none; }

/* ===========================
   PERFIS (Para quem é)
   =========================== */
.perfis-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.perfil-card {
  background: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: var(--radius-lg);
  padding: 36px 28px;
  transition: border-color var(--t), background var(--t);
}
.perfil-card:hover {
  border-color: var(--green-primary);
  background: rgba(31, 105, 58, 0.06);
}
.perfil-tipo {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.perfil-tipo::before {
  content: '';
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--green-accent);
  flex-shrink: 0;
}
.perfil-card ul {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.perfil-card li {
  font-size: 0.875rem;
  color: var(--text-muted);
  line-height: 1.6;
  padding-left: 16px;
  position: relative;
}
.perfil-card li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--green-accent);
  font-size: 0.78rem;
  top: 1px;
}

/* ===========================
   BLOG GRID
   =========================== */
.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.blog-card {
  background: var(--white);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow var(--t), transform var(--t);
}
.blog-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}
.blog-card-img {
  height: 188px;
  background: linear-gradient(135deg, rgba(31, 105, 58, 0.8) 0%, var(--dark-bg) 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.blog-card-img svg {
  color: rgba(132, 194, 91, 0.3);
  width: 64px; height: 64px;
}
.blog-card-body {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.blog-card-date {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--green-primary);
  margin-bottom: 8px;
}
.blog-card-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-dark);
  line-height: 1.3;
  margin-bottom: 10px;
}
.blog-card-excerpt {
  font-size: 0.875rem;
  color: var(--text-gray);
  line-height: 1.65;
  flex: 1;
  margin-bottom: 16px;
}
.blog-card-link {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--green-primary);
  letter-spacing: 0.03em;
  transition: color var(--t), letter-spacing var(--t);
  align-self: flex-start;
}
.blog-card-link:hover { color: var(--green-accent); letter-spacing: 0.05em; }

/* ===========================
   POST CONTENT (artigo)
   =========================== */
.post-header {
  background: var(--dark-bg);
  padding: 120px 0 64px;
  position: relative;
  overflow: hidden;
}
.post-header::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 90% at 85% 50%, rgba(31, 105, 58, 0.18) 0%, transparent 60%);
  pointer-events: none;
}
.post-header-content { position: relative; z-index: 1; max-width: 760px; }
.post-title {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 4vw, 3rem);
  font-weight: 600;
  color: var(--text-light);
  line-height: 1.12;
  margin-bottom: 20px;
  letter-spacing: -0.01em;
}
.post-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.post-meta-date { color: var(--green-accent); }

.post-body {
  background: var(--white);
  padding: 72px 0 96px;
}
.post-content {
  max-width: 720px;
  margin: 0 auto;
  font-size: 1.01rem;
  line-height: 1.82;
  color: var(--text-dark);
}
.post-content h2 {
  font-family: var(--font-display);
  font-size: 1.7rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 52px 0 18px;
  line-height: 1.2;
  letter-spacing: -0.01em;
}
.post-content p { margin-bottom: 22px; }
.post-content ul,
.post-content ol {
  list-style: initial;
  padding-left: 26px;
  margin-bottom: 22px;
}
.post-content li { margin-bottom: 8px; }
.post-content strong { color: var(--green-primary); font-weight: 600; }

.post-cta {
  margin-top: 56px;
  padding: 40px;
  background: var(--light-bg);
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--green-accent);
  border-radius: var(--radius-lg);
  text-align: center;
}
.post-cta h3 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 10px;
}
.post-cta p {
  color: var(--text-gray);
  font-size: 0.92rem;
  margin-bottom: 22px;
}

/* ===========================
   NAVBAR OFFSET
   Compensa a navbar fixa nas páginas internas.
   Aplicado no primeiro elemento de cada página interna.
   =========================== */
.navbar-offset {
  margin-top: 72px; /* altura da navbar scrolled */
}

/* ===========================
   RESPONSIVE — novos componentes
   =========================== */
@media (max-width: 1024px) {
  .perfis-grid { grid-template-columns: 1fr; gap: 14px; }
  .blog-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .page-hero { padding: 100px 0 56px; }
  .perfis-grid { grid-template-columns: 1fr; }
  .blog-grid { grid-template-columns: 1fr; }
  .nav-dropdown-menu {
    position: static;
    opacity: 1;
    pointer-events: all;
    transform: none;
    background: rgba(31, 105, 58, 0.08);
    border: none;
    border-radius: var(--radius);
    padding: 4px 0;
    min-width: auto;
    margin-top: 8px;
  }
  .post-header { padding: 90px 0 48px; }
  .post-body { padding: 48px 0 72px; }
}
```

- [ ] **Step 2: Commit**

```bash
git add css/style.css
git commit -m "feat: add CSS components for service pages, blog, and nav dropdown"
```

---

## Task 10: templates/servico.html

**Files:**
- Modificar: `templates/servico.html` (substituir placeholder da Task 8)

- [ ] **Step 1: Substituir templates/servico.html com template completo**

```html
{% extends 'base.html' %}

{% block title %}{{ servico.meta_title }}{% endblock %}
{% block meta_description %}{{ servico.meta_description }}{% endblock %}
{% block og_title %}{{ servico.meta_title }}{% endblock %}
{% block og_description %}{{ servico.meta_description }}{% endblock %}

{% block extra_head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{{ servico.titulo }}",
  "description": "{{ servico.meta_description }}",
  "provider": {
    "@type": "LocalBusiness",
    "name": "AlarmeForte",
    "telephone": "{{ site.telefone_link }}",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Rio de Janeiro",
      "addressRegion": "RJ",
      "addressCountry": "BR"
    }
  },
  "areaServed": "Rio de Janeiro"
}
</script>
{% endblock %}

{% block content %}

  <!-- BREADCRUMB -->
  <div class="breadcrumb-bar navbar-offset">
    <div class="container">
      <nav class="breadcrumb" aria-label="Navegação estrutural">
        <a href="/">Início</a>
        <span class="breadcrumb-sep" aria-hidden="true">›</span>
        <a href="/#servicos">Serviços</a>
        <span class="breadcrumb-sep" aria-hidden="true">›</span>
        <span class="breadcrumb-current">{{ servico.titulo }}</span>
      </nav>
    </div>
  </div>

  <!-- PAGE HERO -->
  <section class="page-hero">
    <div class="container page-hero-content">
      <span class="section-label">{{ servico.titulo }}</span>
      <h1 class="page-hero-title">{{ servico.titulo }}</h1>
      <p class="page-hero-subtitle">{{ servico.hero_subtitulo }}</p>
      <div class="hero-actions">
        <a href="/#contato" class="btn btn-primary btn-lg">Solicitar Orçamento Gratuito</a>
        <a href="tel:{{ site.telefone_link }}" class="btn btn-outline btn-lg">{{ site.telefone }}</a>
      </div>
    </div>
  </section>

  <!-- O QUE É / COMO FUNCIONA -->
  <section class="section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-label">O que é</span>
        <h2 class="section-title">Como funciona o<br><em>{{ servico.titulo }}</em></h2>
      </div>
      <div style="max-width: 760px; margin: 0 auto;">
        {% for paragrafo in servico.descricao %}
        <p style="font-size: 1rem; color: var(--text-gray); line-height: 1.8; margin-bottom: 22px;">{{ paragrafo }}</p>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- DIFERENCIAIS -->
  <section class="section-dark">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Por que AlarmeForte</span>
        <h2 class="section-title section-title-light">O que nos diferencia<br><em>na prática</em></h2>
      </div>
      <div class="services-grid">
        {% for d in servico.diferenciais %}
        <div class="feature-card reveal">
          <div class="feature-number" aria-hidden="true">0{{ loop.index }}</div>
          <h3>{{ d.titulo }}</h3>
          <p>{{ d.descricao }}</p>
        </div>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- PARA QUEM É -->
  <section class="section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Para quem é</span>
        <h2 class="section-title">{{ servico.titulo }}<br><em>para cada necessidade</em></h2>
      </div>
      <div class="perfis-grid">
        {% for p in servico.perfis %}
        <div class="perfil-card reveal">
          <div class="perfil-tipo">{{ p.tipo }}</div>
          <ul>
            {% for b in p.beneficios %}
            <li>{{ b }}</li>
            {% endfor %}
          </ul>
        </div>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section-light" style="padding-top: 0;">
    <div class="container">
      <div class="section-header">
        <span class="section-label">Dúvidas Frequentes</span>
        <h2 class="section-title">Perguntas sobre<br><em>{{ servico.titulo }}</em></h2>
      </div>
      <div class="faq-list">
        {% for faq in servico.faqs %}
        <div class="faq-item">
          <button class="faq-question" aria-expanded="false">
            {{ faq.pergunta }}
            <svg class="faq-icon" viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
              <path d="M8 3v10M3 8h10"/>
            </svg>
          </button>
          <div class="faq-answer">{{ faq.resposta }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
  </section>

  <!-- CTA FINAL -->
  <section class="section-dark">
    <div class="container" style="text-align: center; max-width: 680px;">
      <span class="section-label">Próximo Passo</span>
      <h2 class="section-title section-title-light" style="margin-bottom: 16px;">
        Pronto para proteger<br><em>o que importa?</em>
      </h2>
      <p style="color: var(--text-muted); margin-bottom: 36px; font-size: 1rem; line-height: 1.7;">
        Diagnóstico gratuito, sem compromisso. Nossa equipe visita o local e apresenta uma proposta personalizada.
      </p>
      <div style="display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;">
        <a href="/#contato" class="btn btn-primary btn-lg">Solicitar Diagnóstico Gratuito</a>
        <a href="https://wa.me/{{ site.whatsapp }}?text=Olá!%20Tenho%20interesse%20em%20{{ servico.titulo | urlencode }}." class="btn btn-outline btn-lg" target="_blank" rel="noopener">Falar no WhatsApp</a>
      </div>
    </div>
  </section>

{% endblock %}

{% block scripts %}
<script>
// FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const answer = btn.nextElementSibling;
    const isOpen = btn.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-question').forEach(b => {
      b.classList.remove('open');
      b.setAttribute('aria-expanded', 'false');
      b.nextElementSibling.classList.remove('open');
    });
    // Open clicked if was closed
    if (!isOpen) {
      btn.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      answer.classList.add('open');
    }
  });
});
</script>
{% endblock %}
```

- [ ] **Step 2: Commit**

```bash
git add templates/servico.html
git commit -m "feat: add servico.html full template with hero, diferenciais, perfis, FAQ"
```

---

## Task 11: Smoke tests de serviço + verificação visual

**Files:**
- Modificar: `tests/test_build.py` (adicionar testes de serviço)

- [ ] **Step 1: Adicionar testes de serviço ao tests/test_build.py**

Abrir `tests/test_build.py` e adicionar ao final do arquivo:

```python
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
```

- [ ] **Step 2: Rodar todos os testes**

```bash
pytest tests/test_build.py -v
```

Saída esperada: todos os testes PASSAM.

- [ ] **Step 3: Verificar visualmente no browser**

```bash
python build.py
python -m http.server 8080
```

Abrir `http://localhost:8080/servicos/cftv/` no browser e verificar: nav com dropdown visível, hero com título, seções de diferenciais e FAQ.

- [ ] **Step 4: Commit**

```bash
git add tests/test_build.py
git commit -m "test: add service page smoke tests"
```

---

## Task 12: CSS blog e atualização dos testes

**Files:**
- `css/style.css` já tem os componentes de blog (adicionados na Task 9)

Verificar que `.blog-grid`, `.blog-card`, `.post-content`, `.post-header` estão presentes no arquivo.

```bash
grep -c "blog-grid" css/style.css
```

Saída esperada: `1` ou mais. Se não encontrar, confirmar que o passo da Task 9 foi executado corretamente.

---

## Task 13: templates/blog-index.html

**Files:**
- Modificar: `templates/blog-index.html` (substituir placeholder da Task 8)

- [ ] **Step 1: Substituir templates/blog-index.html com template completo**

```html
{% extends 'base.html' %}

{% block title %}Blog — Segurança Eletrônica no Rio de Janeiro | AlarmeForte{% endblock %}
{% block meta_description %}Artigos sobre segurança eletrônica no Rio de Janeiro. Dicas de câmeras, alarmes, portaria inteligente e controle de acesso. Blog da AlarmeForte.{% endblock %}

{% block content %}

  <!-- BREADCRUMB -->
  <div class="breadcrumb-bar navbar-offset">
    <div class="container">
      <nav class="breadcrumb" aria-label="Navegação estrutural">
        <a href="/">Início</a>
        <span class="breadcrumb-sep" aria-hidden="true">›</span>
        <span class="breadcrumb-current">Blog</span>
      </nav>
    </div>
  </div>

  <!-- HERO -->
  <section class="page-hero">
    <div class="container page-hero-content">
      <span class="section-label">Blog AlarmeForte</span>
      <h1 class="page-hero-title">Segurança eletrônica<br><em>para o dia a dia</em></h1>
      <p class="page-hero-subtitle">Dicas, novidades e guias práticos sobre câmeras, alarmes, portaria inteligente e controle de acesso para quem vive no Rio de Janeiro.</p>
    </div>
  </section>

  <!-- ARTIGOS -->
  <section class="section-light">
    <div class="container">
      {% if posts %}
      <div class="blog-grid">
        {% for post in posts %}
        <article class="blog-card reveal">
          <div class="blog-card-img" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <div class="blog-card-body">
            <p class="blog-card-date">{{ post.data_publicacao }}</p>
            <h2 class="blog-card-title">{{ post.titulo }}</h2>
            <p class="blog-card-excerpt">{{ post.resumo }}</p>
            <a href="/noticias/{{ post.slug }}/" class="blog-card-link">Ler artigo →</a>
          </div>
        </article>
        {% endfor %}
      </div>
      {% else %}
      <div style="text-align: center; padding: 80px 0;">
        <p style="font-family: var(--font-display); font-size: 1.4rem; color: var(--text-gray); margin-bottom: 24px;">Em breve, novos artigos por aqui.</p>
        <a href="/#contato" class="btn btn-primary btn-lg">Fale com a AlarmeForte</a>
      </div>
      {% endif %}
    </div>
  </section>

  <!-- CTA -->
  <section class="section-dark">
    <div class="container" style="text-align: center; max-width: 640px;">
      <span class="section-label">Diagnóstico Gratuito</span>
      <h2 class="section-title section-title-light" style="margin-bottom: 16px;">Quer proteger sua<br><em>residência ou empresa?</em></h2>
      <p style="color: var(--text-muted); margin-bottom: 36px; font-size: 1rem; line-height: 1.7;">
        Nossa equipe visita o local, identifica vulnerabilidades e apresenta um projeto sob medida — sem custo.
      </p>
      <a href="/#contato" class="btn btn-primary btn-lg">Solicitar Diagnóstico Gratuito</a>
    </div>
  </section>

{% endblock %}
```

- [ ] **Step 2: Commit**

```bash
git add templates/blog-index.html
git commit -m "feat: add blog-index.html template"
```

---

## Task 14: templates/post.html

**Files:**
- Modificar: `templates/post.html` (substituir placeholder da Task 8)

- [ ] **Step 1: Substituir templates/post.html com template completo**

```html
{% extends 'base.html' %}

{% block title %}{{ post.titulo }} | Blog AlarmeForte{% endblock %}
{% block meta_description %}{{ post.meta_description }}{% endblock %}
{% block og_title %}{{ post.titulo }} | AlarmeForte{% endblock %}
{% block og_description %}{{ post.meta_description }}{% endblock %}

{% block extra_head %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ post.titulo }}",
  "description": "{{ post.meta_description }}",
  "datePublished": "{{ post.data_publicacao }}",
  "author": {
    "@type": "Organization",
    "name": "AlarmeForte"
  },
  "publisher": {
    "@type": "Organization",
    "name": "AlarmeForte",
    "url": "{{ site.url }}"
  }
}
</script>
{% endblock %}

{% block content %}

  <!-- BREADCRUMB -->
  <div class="breadcrumb-bar navbar-offset">
    <div class="container">
      <nav class="breadcrumb" aria-label="Navegação estrutural">
        <a href="/">Início</a>
        <span class="breadcrumb-sep" aria-hidden="true">›</span>
        <a href="/noticias/">Blog</a>
        <span class="breadcrumb-sep" aria-hidden="true">›</span>
        <span class="breadcrumb-current">{{ post.titulo }}</span>
      </nav>
    </div>
  </div>

  <!-- POST HEADER -->
  <header class="post-header">
    <div class="container post-header-content">
      <div class="post-meta">
        <span class="post-meta-date">{{ post.data_publicacao }}</span>
        {% if post.tags %}
        <span>·</span>
        {% for tag in post.tags[:3] %}
        <span>{{ tag }}</span>{% if not loop.last %}<span>·</span>{% endif %}
        {% endfor %}
        {% endif %}
      </div>
      <h1 class="post-title">{{ post.titulo }}</h1>
    </div>
  </header>

  <!-- POST BODY -->
  <div class="post-body">
    <div class="container">
      <article class="post-content" id="post-content">
        <!-- Conteúdo markdown convertido para HTML pelo JS abaixo -->
        <div id="post-markdown" style="display:none">{{ post.conteudo }}</div>
      </article>

      <div class="post-cta">
        <h3>Precisa de segurança eletrônica no Rio de Janeiro?</h3>
        <p>A AlarmeForte tem 30 anos de experiência em residências, empresas e condomínios. Diagnóstico gratuito, sem compromisso.</p>
        <div style="display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;">
          <a href="/#contato" class="btn btn-primary">Solicitar Orçamento Gratuito</a>
          <a href="https://wa.me/{{ site.whatsapp }}" class="btn btn-outline" target="_blank" rel="noopener">Falar no WhatsApp</a>
        </div>
      </div>

      <div style="margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--border-light);">
        <a href="/noticias/" style="font-size: 0.875rem; color: var(--green-primary); font-weight: 600; transition: color 0.2s;">← Voltar ao blog</a>
      </div>
    </div>
  </div>

{% endblock %}

{% block scripts %}
<script>
// Converte markdown simples para HTML (sem dependência externa)
(function() {
  var raw = document.getElementById('post-markdown').textContent.trim();
  var html = raw
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]+?<\/li>)/g, function(m) { return '<ul>' + m + '</ul>'; })
    .replace(/<\/ul>\s*<ul>/g, '')
    .split(/\n\n+/)
    .map(function(block) {
      block = block.trim();
      if (block.startsWith('<h') || block.startsWith('<ul>')) return block;
      if (block) return '<p>' + block.replace(/\n/g, ' ') + '</p>';
      return '';
    })
    .join('\n');
  document.getElementById('post-content').innerHTML = html + document.getElementById('post-content').querySelector('.post-cta').outerHTML;

  // Re-attach CTA (was overwritten above) — simpler approach:
  document.getElementById('post-content').innerHTML =
    html +
    document.getElementById('post-content').innerHTML.match(/class="post-cta"[\s\S]*/)?.[0] || '';
})();
</script>
{% endblock %}
```

**Nota:** O script inline de markdown é simples e cobre os padrões gerados pelo agent.py (## H2, **bold**, listas, parágrafos). Não é um parser completo — é suficiente para o conteúdo gerado.

- [ ] **Step 2: Simplificar o script de markdown no post.html**

O script acima tem um bug na re-inserção do CTA. Substituir o bloco `{% block scripts %}` por:

```html
{% block scripts %}
<script>
(function() {
  var container = document.getElementById('post-content');
  var raw = document.getElementById('post-markdown').textContent.trim();
  var html = raw
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[^\n]+<\/li>(\n<li>[^\n]+<\/li>)*)/g, '<ul>$1</ul>')
    .split(/\n\n+/)
    .map(function(b) {
      b = b.trim();
      if (!b) return '';
      if (/^<(h[23]|ul)/.test(b)) return b;
      return '<p>' + b.replace(/\n/g, ' ') + '</p>';
    })
    .filter(Boolean)
    .join('\n');

  var cta = container.querySelector('.post-cta');
  var back = container.querySelector('div[style*="margin-top: 48px"]');
  container.innerHTML = html;
  if (cta) container.appendChild(cta);
  if (back) container.appendChild(back);
})();
</script>
{% endblock %}
```

- [ ] **Step 3: Commit**

```bash
git add templates/post.html
git commit -m "feat: add post.html template with inline markdown renderer"
```

---

## Task 15: Smoke tests blog + verificação

**Files:**
- Modificar: `tests/test_build.py`

- [ ] **Step 1: Adicionar testes de blog ao tests/test_build.py**

Adicionar ao final do arquivo:

```python
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
```

- [ ] **Step 2: Rodar todos os testes**

```bash
pytest tests/ -v
```

Saída esperada: todos os testes PASSAM.

- [ ] **Step 3: Commit**

```bash
git add tests/test_build.py
git commit -m "test: add blog and sitemap smoke tests"
```

---

## Task 16: agent.py

**Files:**
- Criar: `agent.py`

- [ ] **Step 1: Criar agent.py**

```python
"""
agent.py — AlarmeForte V2
Gera rascunhos de post para o blog via Claude API.
Uso: python agent.py --tema "câmeras para casas de veraneio no RJ"
     python agent.py  (gera tema automaticamente)
"""
import anthropic
import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent


def slugify(text: str) -> str:
    """Converte texto para slug URL-safe."""
    text = unicodedata.normalize('NFD', text.lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:80]  # max 80 chars


def generate_post(tema: str | None = None) -> dict:
    """Gera um post completo via Claude API. Retorna dict com os campos do post."""
    client = anthropic.Anthropic()

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

    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2048,
        messages=[{'role': 'user', 'content': prompt}]
    )

    raw = message.content[0].text.strip()

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

    print(f'Gerando artigo: "{args.tema or "tema automático"}"...')
    post = generate_post(args.tema)
    save_draft(post)
    print(f'✅ Rascunho salvo: "{post["titulo"]}" (slug: {post["slug"]})')
```

- [ ] **Step 2: Commit**

```bash
git add agent.py
git commit -m "feat: add agent.py content generator using Claude API"
```

---

## Task 17: tests/test_agent.py

**Files:**
- Criar: `tests/test_agent.py`

- [ ] **Step 1: Criar tests/test_agent.py**

```python
"""Tests para agent.py."""
import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import tempfile
import shutil

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

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=mock_content)]

    with patch('agent.anthropic.Anthropic') as mock_cls:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message
        mock_cls.return_value = mock_client

        post = generate_post('câmeras para condomínios')

    assert post['titulo'] == 'Câmeras para Condomínios no Rio de Janeiro'
    assert post['status'] == 'rascunho'
    assert post['data_publicacao'] is None
    assert 'slug' in post
    assert isinstance(post['tags'], list)


def test_generate_post_handles_json_in_code_block():
    mock_content = '```json\n{"titulo": "Teste", "meta_description": "Desc", "resumo": "Resumo", "conteudo": "## H2\\n\\nTexto.", "tags": ["t"]}\n```'

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=mock_content)]

    with patch('agent.anthropic.Anthropic') as mock_cls:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message
        mock_cls.return_value = mock_client

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
```

- [ ] **Step 2: Rodar os testes do agente**

```bash
pytest tests/test_agent.py -v
```

Saída esperada: todos os 6 testes PASSAM.

- [ ] **Step 3: Commit**

```bash
git add tests/test_agent.py
git commit -m "test: add agent.py tests with mocked Claude API"
```

---

## Task 18: publisher.py

**Files:**
- Criar: `publisher.py`

- [ ] **Step 1: Criar publisher.py**

```python
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
    return json.loads((ROOT / 'data' / 'posts.json').read_text(encoding='utf-8'))


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
```

- [ ] **Step 2: Commit**

```bash
git add publisher.py
git commit -m "feat: add publisher.py with git+deploy automation"
```

---

## Task 19: tests/test_publisher.py

**Files:**
- Criar: `tests/test_publisher.py`

- [ ] **Step 1: Criar tests/test_publisher.py**

```python
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

    saved = json.loads((tmp_path / 'data' / 'posts.json').read_text())
    assert saved['posts'][0]['titulo'] == 'Novo Título'
    assert saved['posts'][0]['conteudo'] == 'Novo conteúdo.'
```

- [ ] **Step 2: Rodar os testes de publisher**

```bash
pytest tests/test_publisher.py -v
```

Saída esperada: todos os 5 testes PASSAM.

- [ ] **Step 3: Rodar todos os testes juntos**

```bash
pytest tests/ -v
```

Saída esperada: todos os testes (build + agent + publisher) PASSAM.

- [ ] **Step 4: Commit**

```bash
git add tests/test_publisher.py
git commit -m "test: add publisher.py tests with mocked subprocess and git"
```

---

## Task 20: admin.py (Painel Streamlit)

**Files:**
- Criar: `admin.py`

- [ ] **Step 1: Criar admin.py**

```python
"""
admin.py — AlarmeForte V2
Painel de controle do blog. Interface para o pai:
  1. Solicitar artigo (informar tema)
  2. Revisar e editar rascunho
  3. Publicar com um clique
Abrir com: abrir-painel.bat
"""
import streamlit as st

from agent import generate_post, save_draft
from publisher import get_drafts, publish_post, update_post_content, discard_post

st.set_page_config(
    page_title='Painel AlarmeForte',
    page_icon='🔒',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# Esconde menu e footer do Streamlit
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Estado da sessão
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'
if 'editing_slug' not in st.session_state:
    st.session_state.editing_slug = None
if 'published_slug' not in st.session_state:
    st.session_state.published_slug = None
if 'error' not in st.session_state:
    st.session_state.error = None


def screen_home():
    st.title('Painel AlarmeForte')
    st.caption('Blog de segurança eletrônica')

    if st.session_state.error:
        st.error(st.session_state.error)
        st.session_state.error = None

    st.markdown('---')
    st.subheader('Novo artigo')
    tema = st.text_input(
        'Sobre o que quer publicar?',
        placeholder='ex: câmeras para casas de veraneio no Rio de Janeiro',
        help='Deixe em branco para o sistema escolher um tema relevante automaticamente.'
    )
    if st.button('Gerar artigo', use_container_width=True, type='primary'):
        with st.spinner('Gerando artigo com IA... (aguarde ~20 segundos)'):
            try:
                post = generate_post(tema if tema.strip() else None)
                save_draft(post)
                st.success(f'Rascunho criado: "{post["titulo"]}"')
                st.rerun()
            except Exception as e:
                st.error(f'Erro ao gerar artigo: {e}')

    st.markdown('---')
    rascunhos = get_drafts()

    if rascunhos:
        st.subheader(f'Aguardando revisão ({len(rascunhos)})')
        for post in rascunhos:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f'**{post["titulo"]}**')
                    st.caption(f'Gerado em {post["data_criacao"]}')
                with col2:
                    if st.button('Revisar', key=f'rev_{post["slug"]}', use_container_width=True):
                        st.session_state.screen = 'review'
                        st.session_state.editing_slug = post['slug']
                        st.rerun()
    else:
        st.info('Nenhum rascunho aguardando revisão. Gere um novo artigo acima.')


def screen_review():
    slug = st.session_state.editing_slug
    rascunhos = get_drafts()
    post = next((p for p in rascunhos if p['slug'] == slug), None)

    if not post:
        st.session_state.screen = 'home'
        st.rerun()
        return

    if st.button('← Voltar'):
        st.session_state.screen = 'home'
        st.rerun()

    st.title('Revisar artigo')
    st.markdown('---')

    titulo = st.text_input('Título', value=post['titulo'])
    conteudo = st.text_area(
        'Conteúdo',
        value=post['conteudo'],
        height=480,
        help='Você pode editar o texto antes de publicar. Linhas começando com ## são títulos de seção.'
    )

    st.markdown('---')
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Descartar', use_container_width=True):
            discard_post(slug)
            st.session_state.screen = 'home'
            st.rerun()

    with col2:
        if st.button('Publicar agora', use_container_width=True, type='primary'):
            # Salva edições
            try:
                update_post_content(slug, titulo, conteudo)
            except Exception as e:
                st.error(f'Erro ao salvar edições: {e}')
                return

            # Publica
            with st.spinner('Publicando no site... (aguarde ~30 segundos)'):
                try:
                    publish_post(slug)
                    st.session_state.published_slug = slug
                    st.session_state.screen = 'success'
                    st.rerun()
                except Exception as e:
                    st.session_state.error = f'Erro ao publicar: {e}. Verifique se o repositório Git está configurado.'
                    st.session_state.screen = 'home'
                    st.rerun()


def screen_success():
    st.markdown('<br>' * 3, unsafe_allow_html=True)
    st.success('Artigo publicado com sucesso!')
    st.write('O site será atualizado em aproximadamente 30 segundos.')

    site_url = 'https://alarmeforte.com.br'
    slug = st.session_state.published_slug
    if slug:
        st.link_button('Ver no site', f'{site_url}/noticias/{slug}/')

    st.markdown('<br>', unsafe_allow_html=True)
    if st.button('Criar outro artigo', use_container_width=True, type='primary'):
        st.session_state.screen = 'home'
        st.session_state.editing_slug = None
        st.session_state.published_slug = None
        st.rerun()


# Router
screens = {
    'home': screen_home,
    'review': screen_review,
    'success': screen_success,
}
screens.get(st.session_state.screen, screen_home)()
```

- [ ] **Step 2: Testar manualmente o painel**

```bash
streamlit run admin.py
```

Verificar no browser:
- Tela inicial carrega sem erros
- Campo de tema está visível
- Botão "Gerar artigo" aparece

Fechar com `Ctrl+C`.

- [ ] **Step 3: Commit**

```bash
git add admin.py
git commit -m "feat: add admin.py Streamlit panel for blog management"
```

---

## Task 21: abrir-painel.bat

**Files:**
- Criar: `abrir-painel.bat`

- [ ] **Step 1: Criar abrir-painel.bat**

```bat
@echo off
title Painel AlarmeForte
start "" /MIN python -m streamlit run admin.py --server.headless true --server.port 8502 --browser.gatherUsageStats false
ping -n 4 127.0.0.1 > nul
start http://localhost:8502
```

**Explicação:**
- `start "" /MIN` — abre o processo em janela minimizada na barra de tarefas
- `ping -n 4` — aguarda ~3 segundos para o Streamlit iniciar
- `start http://localhost:8502` — abre o browser automaticamente

- [ ] **Step 2: Testar o .bat**

Dar duplo clique em `abrir-painel.bat`. Verificar que:
1. Uma janela minimizada aparece na barra de tarefas
2. O browser abre em `http://localhost:8502` com o painel

- [ ] **Step 3: Commit**

```bash
git add abrir-painel.bat
git commit -m "feat: add abrir-painel.bat launcher"
```

---

## Task 22: Nav dropdown — main.js

**Files:**
- Modificar: `js/main.js`

- [ ] **Step 1: Ler js/main.js para entender o código existente**

Abrir o arquivo e verificar a estrutura atual (nav scroll, hamburger, reveal, counters, form).

- [ ] **Step 2: Adicionar comportamento de dropdown ao final de js/main.js**

Adicionar ao final do arquivo (após o último bloco de código existente):

```javascript
// ===========================
// NAV DROPDOWN
// ===========================
(function () {
  var wrappers = document.querySelectorAll('.nav-dropdown-wrapper');

  wrappers.forEach(function (wrapper) {
    var toggle = wrapper.querySelector('.nav-dropdown-toggle');
    var menu = wrapper.querySelector('.nav-dropdown-menu');

    if (!toggle || !menu) return;

    // Desktop: hover
    wrapper.addEventListener('mouseenter', function () {
      wrapper.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
    });
    wrapper.addEventListener('mouseleave', function () {
      wrapper.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });

    // Click (mobile e teclado)
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = wrapper.classList.contains('open');
      // Fecha todos
      wrappers.forEach(function (w) {
        w.classList.remove('open');
        var t = w.querySelector('.nav-dropdown-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
      // Abre este se estava fechado
      if (!isOpen) {
        wrapper.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Fecha dropdown ao clicar fora
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown-wrapper')) {
      wrappers.forEach(function (w) {
        w.classList.remove('open');
        var t = w.querySelector('.nav-dropdown-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });
})();
```

- [ ] **Step 3: Verificar visualmente**

```bash
python build.py && python -m http.server 8080
```

Abrir `http://localhost:8080` e verificar:
- Hover em "Serviços" na nav abre o dropdown com os 6 serviços
- Clicar em um serviço navega para a página correta
- No mobile (DevTools), o dropdown funciona via clique

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "feat: add nav dropdown behavior to main.js"
```

---

## Task 23: Atualizar iniciar.bat + teste final

**Files:**
- Modificar: `iniciar.bat`

- [ ] **Step 1: Ler iniciar.bat atual**

Verificar conteúdo do arquivo existente.

- [ ] **Step 2: Substituir iniciar.bat para rodar build antes do server**

```bat
@echo off
echo Gerando site...
python build.py
echo.
echo Servidor local em http://localhost:8080
echo Pressione Ctrl+C para parar.
start http://localhost:8080
python -m http.server 8080
```

- [ ] **Step 3: Rodar suite completa de testes**

```bash
pytest tests/ -v --tb=short
```

Saída esperada: todos os testes PASSAM. Output final similar a:
```
tests/test_agent.py::test_slugify_removes_accents PASSED
tests/test_agent.py::test_generate_post_returns_required_fields PASSED
...
tests/test_build.py::test_build_exits_successfully PASSED
...
tests/test_publisher.py::test_publish_post_updates_status PASSED
...
== N passed in X.XXs ==
```

- [ ] **Step 4: Rodar build completo e inspecionar output**

```bash
python build.py
```

Saída esperada:
```
Building AlarmeForte V2...
  ✓ index.html
  ✓ servicos/cftv/index.html
  ✓ servicos/alarme-monitorado/index.html
  ✓ servicos/portaria-inteligente/index.html
  ✓ servicos/interfonia/index.html
  ✓ servicos/controle-acesso/index.html
  ✓ servicos/monitoramento-remoto/index.html
  ✓ noticias/index.html
  ✓ sitemap.xml
  ✓ robots.txt

✅ Build completo — 9 páginas geradas
```

- [ ] **Step 5: Verificação visual completa**

```bash
python -m http.server 8080
```

Verificar no browser:
- `http://localhost:8080/` — homepage com nav dropdown funcional
- `http://localhost:8080/servicos/cftv/` — hero, diferenciais, perfis, FAQ accordion
- `http://localhost:8080/servicos/portaria-inteligente/` — mesma estrutura, conteúdo diferente
- `http://localhost:8080/noticias/` — tela de "em breve" com CTA
- Mobile (Chrome DevTools, 375px): nav hamburger, perfis em coluna, blog grid em coluna

- [ ] **Step 6: Commit final**

```bash
git add iniciar.bat
git commit -m "feat: update iniciar.bat to run build before serving"
git tag v2.0.0
```

---

## Verificação Final (Checklist)

Antes de declarar o V2 completo, verificar:

- [ ] `python build.py` gera 9 arquivos sem erros
- [ ] `pytest tests/ -v` — todos os testes passam
- [ ] Homepage: nav dropdown com 6 serviços funciona
- [ ] Cada página de serviço: hero, breadcrumb, diferenciais, perfis, FAQ
- [ ] FAQ accordion abre/fecha corretamente
- [ ] Blog index: carrega sem erros (estado vazio)
- [ ] Mobile (375px): nav, service pages, blog — sem overflow
- [ ] `sitemap.xml` contém todas as URLs de serviço
- [ ] `abrir-painel.bat` abre painel Streamlit no browser
- [ ] Painel: gerar artigo → rascunho aparece na lista → tela de revisão carrega

---

## Configuração pós-deploy (fora deste plano)

Após aprovação do pai e antes de apontar o domínio:
1. Criar repositório GitHub privado
2. `git remote add origin https://github.com/seu-user/alarmeforte-site.git && git push -u origin main`
3. Conectar no Netlify → New site from Git → selecionar repo → publish directory: `.` (raiz)
4. Configurar domínio `alarmeforte.com.br` nas DNS settings do Netlify
5. Criar `.env` com `ANTHROPIC_API_KEY` e `NETLIFY_DEPLOY_HOOK`
6. Substituir `YOUR_FORMSPREE_ID` no `templates/homepage.html` pelo ID real do Formspree
