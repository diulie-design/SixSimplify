import streamlit as st
import time
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Foco no Foco", layout="wide")

# ESTILO
st.markdown("""
<style>
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    section.main > div {
        background-color: #f4f7fb;
    }

    h1, h2, h3 {
        color: #003b71;
        font-weight: 800;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
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
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
    }

    div[data-testid="stTextInput"] input {
        font-size: 20px;
        height: 56px;
        border-radius: 12px;
    }

    textarea {
        font-size: 18px !important;
        border-radius: 12px !important;
    }

    .bloco-azul {
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
        padding: 24px;
        border-radius: 18px;
        margin: 12px 0 20px 0;
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
    }

    .foco-final {
        font-size: 34px;
        font-weight: 900;
        line-height: 1.25;
    }

    .info-equipe {
        font-size: 18px;
        line-height: 1.6;
    }

    .card-section {
        background: white;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.07);
        border: 1px solid #e6edf5;
        margin-bottom: 24px;
    }

    .postit {
        background: linear-gradient(180deg, #fff8c9 0%, #fff2a8 100%);
        padding: 22px;
        border-radius: 16px;
        min-height: 180px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        margin-bottom: 10px;
        color: #1f2937;
        border-left: 8px solid #003b71;
    }

    .postit h4 {
        color: #003b71;
        font-size: 18px;
        margin-bottom: 14px;
    }

    .postit-texto {
        color: #1f2937;
        font-size: 20px;
        line-height: 1.5;
        font-weight: 700;
    }

    .votos {
        color: #003b71;
        font-weight: 800;
        margin-top: 12px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        border: none;
        background: linear-gradient(135deg, #003b71, #005a9c);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

# BANCO
conn = sqlite3.connect("postits.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS postits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipe TEXT,
    texto TEXT,
    votos INTEGER DEFAULT 0,
    ativo INTEGER DEFAULT 1
)
""")
conn.commit()

try:
    cursor.execute("ALTER TABLE postits ADD COLUMN votos INTEGER DEFAULT 0")
    conn.commit()
except:
    pass

try:
    cursor.execute("ALTER TABLE postits ADD COLUMN ativo INTEGER DEFAULT 1")
    conn.commit()
except:
    pass


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


def buscar_mais_votados():
    cursor.execute("""
    SELECT id, equipe, texto, votos
    FROM postits
    WHERE ativo = 1
    ORDER BY votos DESC
    """)

    dados = cursor.fetchall()

    if not dados:
        return [], 0, False

    maior_voto = dados[0][3]

    if maior_voto == 0:
        return [], 0, False

    empatados = [item for item in dados if item[3] == maior_voto]

    tem_empate = len(empatados) > 1

    return empatados, maior_voto, tem_empate


# FOCO PRINCIPAL
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
    st.markdown(
        f"""
<div class="bloco-azul foco-final">
{st.session_state.foco_salvo}
</div>
""",
        unsafe_allow_html=True
    )

    if st.button("Editar foco"):
        st.session_state.editando_foco = True
        st.rerun()

st.divider()

# ABAS
aba1, aba2 = st.tabs([
    "🎯 Foco no Foco",
    "🚧 Principais Obstáculos"
])

with aba1:

    st.title("Foco no Foco")

    # CADASTRO
    st.markdown('<div class="card-section">', unsafe_allow_html=True)

    st.subheader("Cadastro da equipe")

    if "nome_equipe_salvo" not in st.session_state:
        st.session_state.nome_equipe_salvo = ""

    if "lider_equipe_salvo" not in st.session_state:
        st.session_state.lider_equipe_salvo = ""

    if "editando_equipe" not in st.session_state:
        st.session_state.editando_equipe = True

    tempo_cadastro_minutos = st.number_input(
        "Tempo para cadastrar equipe e líder",
        min_value=1,
        max_value=60,
        value=1
    )

    mostrar_cronometro(
        "timer_cadastro",
        int(tempo_cadastro_minutos * 60)
    )

    if st.session_state.editando_equipe:

        nome_equipe_digitado = st.text_input(
            "Nome da equipe",
            value=st.session_state.nome_equipe_salvo
        )

        lider_equipe_digitado = st.text_input(
            "Líder da equipe",
            value=st.session_state.lider_equipe_salvo
        )

        if st.button("Salvar equipe"):

            st.session_state.nome_equipe_salvo = nome_equipe_digitado
            st.session_state.lider_equipe_salvo = lider_equipe_digitado
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

    # POST-ITS
    st.markdown('<div class="card-section">', unsafe_allow_html=True)

    st.subheader("Post-its das equipes")

    tempo_postit_minutos = st.number_input(
        "Tempo para preencher os post-its",
        min_value=1,
        max_value=60,
        value=5
    )

    mostrar_cronometro(
        "timer_postit",
        int(tempo_postit_minutos * 60)
    )

    novo_postit = st.text_area(
        "Adicionar post-it",
        placeholder="Digite exatamente 6 palavras"
    )

    qtd_palavras = contar_palavras(novo_postit)

    st.caption(f"{qtd_palavras}/6 palavras")

    if qtd_palavras < 6 and qtd_palavras > 0:
        st.warning("O post-it deve ter exatamente 6 palavras.")

    if qtd_palavras > 6:
        st.error("O post-it deve ter exatamente 6 palavras.")

    if st.button("Adicionar post-it"):

        if qtd_palavras != 6:
            st.error("O post-it precisa ter exatamente 6 palavras.")

        else:

            cursor.execute("""
            INSERT INTO postits (equipe, texto, votos, ativo)
            VALUES (?, ?, 0, 1)
            """, (nome_equipe, novo_postit))

            conn.commit()

            st.success("Post-it adicionado!")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # FOCO NO FOCO RESULTADO
    st.subheader("Votação")

    st.markdown("## Foco no Foco")

    vencedores, maior_voto, tem_empate = buscar_mais_votados()

    if vencedores and not tem_empate:

        st.markdown(
            f"""
<div class="bloco-azul foco-final">
{vencedores[0][2]}
</div>
""",
            unsafe_allow_html=True
        )

    elif tem_empate:

        st.warning(
            "Houve empate entre os post-its mais votados. Faça uma nova votação apenas com os empatados."
        )

        if st.button("Iniciar nova votação com os empatados"):

            ids_empatados = [str(item[0]) for item in vencedores]

            cursor.execute("UPDATE postits SET ativo = 0")

            cursor.execute(
                f"""
                UPDATE postits
                SET ativo = 1, votos = 0
                WHERE id IN ({",".join(ids_empatados)})
                """
            )

            conn.commit()
            st.rerun()

    else:
        st.info("O Foco no Foco aparecerá aqui após a votação.")

    # CONTROLES
    col_reset1, col_reset2 = st.columns(2)

    with col_reset1:
        if st.button("Zerar votos"):
            cursor.execute("UPDATE postits SET votos = 0")
            conn.commit()
            st.rerun()

    with col_reset2:
        if st.button("Mostrar todos novamente"):
            cursor.execute("UPDATE postits SET ativo = 1")
            conn.commit()
            st.rerun()

    # MURAL
    cursor.execute("""
    SELECT id, equipe, texto, votos
    FROM postits
    WHERE ativo = 1
    ORDER BY id DESC
    """)

    postits = cursor.fetchall()

    if postits:

        colunas = st.columns(3)

        for i, (postit_id, equipe, texto, votos) in enumerate(postits):

            with colunas[i % 3]:

                st.markdown(
                    f"""
<div class="postit">
<h4>{equipe}</h4>
<div class="postit-texto">{texto}</div>
<div class="votos">Votos: {votos}</div>
</div>
""",
                    unsafe_allow_html=True
                )

                if st.button(
                    "Votar neste post-it",
                    key=f"votar_{postit_id}"
                ):

                    cursor.execute("""
                    UPDATE postits
                    SET votos = votos + 1
                    WHERE id = ?
                    """, (postit_id,))

                    conn.commit()
                    st.rerun()

    else:
        st.info("Nenhum post-it disponível.")

with aba2:

    st.title("Principais Obstáculos")

    st.info(
        "Essa aba está reservada para a próxima etapa."
    )
