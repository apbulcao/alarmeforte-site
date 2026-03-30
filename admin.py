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
            try:
                update_post_content(slug, titulo, conteudo)
            except Exception as e:
                st.error(f'Erro ao salvar edições: {e}')
                return

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
