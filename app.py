import streamlit as st
import time
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Foco no Foco", layout="wide")

# =========================
# ESTILO
# =========================

st.markdown("""
<style>

.main .block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

section.main > div {
    background: #f7f9fc;
}

hr {
    display: none;
}

h1 {
    color: #002f5f;
    font-size: 42px !important;
    font-weight: 800;
}

h2 {
    color: #002f5f;
    font-size: 30px !important;
    font-weight: 750;
}

h3 {
    color: #002f5f;
    font-size: 24px !important;
    font-weight: 700;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 16px;
    background: transparent;
    margin-bottom: 24px;
}

.stTabs [data-baseweb="tab"] {
    min-height: 70px;
    padding: 0 34px;
    background: #ffffff;
    border-radius: 18px;
    color: #002f5f;
    font-weight: 800;
    font-size: 24px;
    border: 1px solid #dbe4ef;
}

.stTabs [aria-selected="true"] {
    background: #002f5f;
    color: white;
    border: 1px solid #002f5f;
}

.bloco-azul {
    background: #002f5f;
    color: white;
    padding: 28px 32px;
    border-radius: 22px;
    margin: 14px 0 24px 0;
}

.foco-final {
    font-size: 34px;
    font-weight: 850;
    line-height: 1.25;
}

.info-equipe {
    font-size: 20px;
    line-height: 1.7;
}

div[data-testid="stTextInput"] input {
    font-size: 22px;
    height: 62px;
    border-radius: 16px;
    border: 1px solid #cfd9e6;
    background-color: #ffffff;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #6b7280 !important;
}

textarea {
    font-size: 20px !important;
    border-radius: 16px !important;
    border: 1px solid #cfd9e6 !important;
    color: #111827 !important;
    background-color: #ffffff !important;
}

textarea::placeholder {
    color: #6b7280 !important;
}

.stNumberInput input {
    font-size: 20px;
    height: 56px;
    border-radius: 14px;
    color: #111827 !important;
    background-color: #ffffff !important;
}

.stButton > button {
    width: 100%;
    min-height: 56px;
    border-radius: 16px;
    border: 1px solid #002f5f;
    background: #002f5f;
    color: white;
    font-weight: 750;
    font-size: 18px;
}

.stButton > button:hover {
    background: #00447f;
    border-color: #00447f;
}

.postit {
    background: #fff6b8;
    padding: 24px;
    border-radius: 20px;
    min-height: 180px;
    margin-bottom: 18px;
    color: #1f2937;
    border: 1px solid #f0dc7a;
}

.postit-votado {
    background: #d9fbe3;
    padding: 24px;
    border-radius: 20px;
    min-height: 180px;
    margin-bottom: 18px;
    color: #1f2937;
    border: 2px solid #16a34a;
}

.postit h4,
.postit-votado h4 {
    color: #002f5f;
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 14px;
    font-weight: 800;
}

.postit-texto {
    color: #111827;
    font-size: 22px;
    line-height: 1.45;
    font-weight: 750;
}

.votos {
    color: #002f5f;
    font-size: 18px;
    font-weight: 800;
    margin-top: 16px;
}

@media (max-width: 768px) {

    h1 {
        font-size: 34px !important;
    }

    h2 {
        font-size: 28px !important;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 76px;
        font-size: 26px;
        padding: 0 24px;
    }

    .postit-texto {
        font-size: 24px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# BANCO
# =========================

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

# =========================
# FUNÇÕES
# =========================

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

        tempo_restante = max(
            tempo_total_segundos - tempo_passado,
            0
        )

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

    empatados = [
        item for item in dados
        if item[3] == maior_voto
    ]

    tem_empate = len(empatados) > 1

    return empatados, maior_voto, tem_empate

# =========================
# SESSION STATE
# =========================

if "postits_votados" not in st.session_state:
    st.session_state.postits_votados = set()

if "foco_salvo" not in st.session_state:
    st.session_state.foco_salvo = ""

if "editando_foco" not in st.session_state:
    st.session_state.editando_foco = True

# =========================
# FOCO
# =========================

st.markdown("## Foco")

if st.session_state.editando_foco:

    foco_digitado = st.text_input(
        label="campo_foco",
        value=st.session_state.foco_salvo,
        placeholder="Digite aqui o título do foco",
        key="campo_foco",
        label_visibility="collapsed"
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
<div class="bloco-azul foco-final">
{st.session_state.foco_salvo}
</div>
""",
        unsafe_allow_html=True
    )

    if st.button("Editar foco"):

        st.session_state.editando_foco = True

        st.rerun()

# =========================
# PÁGINA PRINCIPAL
# =========================

st.title("Foco no Foco")

# =====================
# CADASTRO EQUIPE
# =====================

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
        value=st.session_state.nome_equipe_salvo,
        placeholder="Digite o nome da equipe"
    )

    lider_equipe_digitado = st.text_input(
        "Líder da equipe",
        value=st.session_state.lider_equipe_salvo,
        placeholder="Digite o nome do líder"
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

# =====================
# POST ITS
# =====================

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

# =====================
# MURAL
# =====================

cursor.execute("""
SELECT id, equipe, texto, votos
FROM postits
WHERE ativo = 1
ORDER BY id DESC
""")

postits = cursor.fetchall()

if postits:

    st.subheader("Post-its em votação")

    colunas = st.columns(3)

    for i, (postit_id, equipe, texto, votos) in enumerate(postits):

        with colunas[i % 3]:

            classe_postit = (
                "postit-votado"
                if postit_id in st.session_state.postits_votados
                else "postit"
            )

            st.markdown(
                f"""
<div class="{classe_postit}">
<h4>{equipe}</h4>
<div class="postit-texto">{texto}</div>
<div class="votos">Votos: {votos}</div>
</div>
""",
                unsafe_allow_html=True
            )

            if postit_id in st.session_state.postits_votados:

                if st.button(
                    "Desfazer voto",
                    key=f"desfazer_{postit_id}"
                ):

                    cursor.execute("""
                    UPDATE postits
                    SET votos = CASE
                        WHEN votos > 0 THEN votos - 1
                        ELSE 0
                    END
                    WHERE id = ?
                    """, (postit_id,))

                    conn.commit()

                    st.session_state.postits_votados.remove(postit_id)

                    st.rerun()

            else:

                if st.button(
                    "Votar",
                    key=f"votar_{postit_id}"
                ):

                    cursor.execute("""
                    UPDATE postits
                    SET votos = votos + 1
                    WHERE id = ?
                    """, (postit_id,))

                    conn.commit()

                    st.session_state.postits_votados.add(postit_id)

                    st.rerun()

else:

    st.info("Nenhum post-it disponível.")

# =====================
# RESULTADO
# =====================

st.subheader("Resultado da votação")

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

        st.session_state.postits_votados = set()

        st.rerun()

else:

    st.info("O Foco no Foco aparecerá aqui após a votação.")

col_reset1, col_reset2 = st.columns(2)

with col_reset1:

    if st.button("Zerar votos"):

        cursor.execute("UPDATE postits SET votos = 0")

        conn.commit()

        st.session_state.postits_votados = set()

        st.rerun()

with col_reset2:

    if st.button("Mostrar todos novamente"):

        cursor.execute("UPDATE postits SET ativo = 1")

        conn.commit()

        st.session_state.postits_votados = set()

        st.rerun()
