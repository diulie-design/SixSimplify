import streamlit as st
import time
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Foco no Foco", layout="wide")

# ESTILO PROFISSIONAL
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    section.main > div {
        background-color: #f4f7fb;
    }

    h1 {
        color: #003b71;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #003b71;
        font-weight: 700;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding-bottom: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 58px;
        padding: 0px 28px;
        background: white;
        border-radius: 14px;
        color: #003b71;
        font-weight: 700;
        font-size: 17px;
        border: 1px solid #d9e2ec;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        transition: all 0.2s ease-in-out;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
        border: none;
        box-shadow: 0 6px 16px rgba(0, 59, 113, 0.25);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #eef4fa;
        transform: translateY(-1px);
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        border: none;
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    }

    div[data-testid="stTextInput"] input {
        font-size: 20px;
        height: 56px;
        border-radius: 12px;
        border: 1px solid #d0d7e2;
        background-color: white;
        padding-left: 14px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }

    textarea {
        font-size: 18px !important;
        border-radius: 12px !important;
        border: 1px solid #d0d7e2 !important;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04) !important;
    }

    .bloco-azul {
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
        padding: 24px;
        border-radius: 18px;
        margin: 12px 0 20px 0;
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    }

    .foco-salvo {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.25;
    }

    .info-equipe {
        font-size: 18px;
        line-height: 1.6;
    }

    .postit {
        background: linear-gradient(180deg, #fff8c9 0%, #fff2a8 100%);
        padding: 22px;
        border-radius: 16px;
        min-height: 180px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        margin-bottom: 22px;
        color: #1f2937;
        font-family: Arial, sans-serif;
        overflow-wrap: break-word;
        word-break: break-word;
        white-space: normal;
        border-left: 8px solid #003b71;
        transition: all 0.2s ease-in-out;
    }

    .postit:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.16);
    }

    .postit h4 {
        margin-top: 0;
        margin-bottom: 14px;
        font-size: 18px;
        color: #003b71;
    }

    .postit-texto {
        color: #1f2937;
        font-size: 20px;
        line-height: 1.5;
        font-weight: 700;
    }

    .card-section {
        background: white;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.07);
        border: 1px solid #e6edf5;
        margin-bottom: 24px;
    }

    .timer-box {
        background: white;
        padding: 18px 22px;
        border-radius: 16px;
        border: 1px solid #e1e8f0;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# BANCO DE DADOS
conn = sqlite3.connect("postits.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS postits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipe TEXT,
    texto TEXT
)
""")
conn.commit()


def contar_palavras(texto):
    return len(texto.strip().split())


def mostrar_cronometro(nome_timer, tempo_total_segundos):
    if nome_timer not in st.session_state:
        st.session_state[nome_timer] = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Iniciar cronômetro", key=f"iniciar_{nome_timer}"):
            st.session_state[nome_timer] = time.time()

    with col2:
        if st.button("Encerrar cronômetro", key=f"encerrar_{nome_timer}"):
            st.session_state[nome_timer] = None
            st.warning("Cronômetro encerrado.")

    if st.session_state[nome_timer]:
        st_autorefresh(interval=1000, key=f"refresh_{nome_timer}")

        tempo_passado = int(time.time() - st.session_state[nome_timer])
        tempo_restante = max(tempo_total_segundos - tempo_passado, 0)

        minutos = tempo_restante // 60
        segundos = tempo_restante % 60

        st.markdown(f"## ⏱️ {minutos:02d}:{segundos:02d}")
        st.progress(tempo_restante / tempo_total_segundos)

        if tempo_restante == 0:
            st.error("Tempo encerrado!")
            st.session_state[nome_timer] = None


# FOCO FORA DAS ABAS
if "foco_salvo" not in st.session_state:
    st.session_state.foco_salvo = ""

if "editando_foco" not in st.session_state:
    st.session_state.editando_foco = True

st.markdown("## Foco")

if st.session_state.editando_foco:
    foco_digitado = st.text_input(
        " ",
        value=st.session_state.foco_salvo,
        placeholder="Digite aqui o título do foco",
        key="campo_foco"
    )

    if st.button("Salvar foco"):
        if foco_digitado.strip():
            st.session_state.foco_salvo = foco_digitado.strip()
            st.session_state.editando_foco = False
            st.rerun()
        else:
            st.warning("Digite um foco antes de salvar.")

else:
    st.markdown(
        f"""
<div class="bloco-azul foco-salvo">
{st.session_state.foco_salvo}
</div>
""",
        unsafe_allow_html=True
    )

    if st.button("Editar foco"):
        st.session_state.editando_foco = True
        st.rerun()

st.divider()


aba1, aba2 = st.tabs([
    "🎯 Foco no Foco",
    "🚧 Principais Obstáculos"
])


with aba1:
    st.title("Foco no Foco")

    st.markdown('<div class="card-section">', unsafe_allow_html=True)

    st.subheader("Cadastro da equipe")

    if "nome_equipe_salvo" not in st.session_state:
        st.session_state.nome_equipe_salvo = ""

    if "lider_equipe_salvo" not in st.session_state:
        st.session_state.lider_equipe_salvo = ""

    if "editando_equipe" not in st.session_state:
        st.session_state.editando_equipe = True

    tempo_cadastro_minutos = st.number_input(
        "Tempo para cadastrar equipe e líder em minutos",
        min_value=1,
        max_value=60,
        value=1,
        step=1
    )

    mostrar_cronometro(
        nome_timer="timer_cadastro",
        tempo_total_segundos=int(tempo_cadastro_minutos * 60)
    )

    if st.session_state.editando_equipe:
        nome_equipe_digitado = st.text_input(
            "Nome da equipe",
            value=st.session_state.nome_equipe_salvo,
            placeholder="Digite o nome da equipe",
            key="campo_nome_equipe"
        )

        lider_equipe_digitado = st.text_input(
            "Líder da equipe",
            value=st.session_state.lider_equipe_salvo,
            placeholder="Digite o nome do líder",
            key="campo_lider_equipe"
        )

        if st.button("Salvar equipe"):
            if not nome_equipe_digitado.strip():
                st.warning("Digite o nome da equipe antes de salvar.")
            elif not lider_equipe_digitado.strip():
                st.warning("Digite o nome do líder antes de salvar.")
            else:
                st.session_state.nome_equipe_salvo = nome_equipe_digitado.strip()
                st.session_state.lider_equipe_salvo = lider_equipe_digitado.strip()
                st.session_state.editando_equipe = False
                st.rerun()

    else:
        st.markdown(
            f"""
<div class="bloco-azul info-equipe">
<strong>Equipe:</strong> {st.session_state.nome_equipe_salvo}<br>
<strong>Líder:</strong> {st.session_state.lider_equipe_salvo}
</div>
""",
            unsafe_allow_html=True
        )

        if st.button("Editar equipe"):
            st.session_state.editando_equipe = True
            st.rerun()

    nome_equipe = st.session_state.nome_equipe_salvo

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card-section">', unsafe_allow_html=True)

    st.subheader("Post-its das equipes")

    tempo_postit_minutos = st.number_input(
        "Tempo para preencher os post-its em minutos",
        min_value=1,
        max_value=60,
        value=5,
        step=1
    )

    mostrar_cronometro(
        nome_timer="timer_postit",
        tempo_total_segundos=int(tempo_postit_minutos * 60)
    )

    novo_postit = st.text_area(
        "Adicionar post-it",
        placeholder="Digite uma ideia com exatamente 6 palavras"
    )

    qtd_palavras = contar_palavras(novo_postit)

    st.caption(f"{qtd_palavras}/6 palavras")

    if qtd_palavras < 6 and qtd_palavras > 0:
        st.warning("O post-it deve ter exatamente 6 palavras.")

    if qtd_palavras > 6:
        st.error("O post-it deve ter exatamente 6 palavras.")

    if st.button("Adicionar post-it"):
        if not nome_equipe.strip():
            st.warning("Preencha e salve o nome da equipe antes de adicionar um post-it.")
        elif not novo_postit.strip():
            st.warning("Digite o conteúdo do post-it.")
        elif qtd_palavras != 6:
            st.error("O post-it precisa ter exatamente 6 palavras.")
        else:
            cursor.execute(
                "INSERT INTO postits (equipe, texto) VALUES (?, ?)",
                (nome_equipe, novo_postit)
            )
            conn.commit()
            st.success("Post-it adicionado!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    cursor.execute("SELECT equipe, texto FROM postits ORDER BY id DESC")
    postits = cursor.fetchall()

    if postits:
        st.subheader("Mural de post-its")

        colunas = st.columns(3)

        for i, (equipe, texto) in enumerate(postits):
            with colunas[i % 3]:
                st.markdown(
                    f"""
<div class="postit">
<h4>{equipe}</h4>
<div class="postit-texto">{texto}</div>
</div>
""",
                    unsafe_allow_html=True
                )
    else:
        st.info("Nenhum post-it adicionado ainda.")


with aba2:
    st.title("Principais Obstáculos")

    st.markdown(
        """
<div class="card-section">
<h3>Etapa em construção</h3>
<p style="font-size:18px; color:#4b5563;">
Essa aba está reservada para a próxima etapa da dinâmica.
</p>
</div>
""",
        unsafe_allow_html=True
    )
