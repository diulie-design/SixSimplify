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
    max-width: 1000px;
    padding-top: 1.5rem;
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
    font-size: 40px !important;
    font-weight: 850;
}

h2 {
    color: #002f5f;
    font-size: 30px !important;
    font-weight: 800;
}

h3 {
    color: #002f5f;
    font-size: 26px !important;
    font-weight: 800;
}

/* ABAS */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    margin-bottom: 24px;
}

.stTabs [data-baseweb="tab"] {
    min-height: 68px;
    padding: 0 18px;
    background: #ffffff;
    border-radius: 18px;
    color: #002f5f;
    font-weight: 800;
    border: 2px solid #dbe4ef;
}

.stTabs [data-baseweb="tab"] p {
    font-size: 21px !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
}

.stTabs [aria-selected="true"] {
    background: #002f5f;
    color: white;
    border: 2px solid #002f5f;
}

.stTabs [aria-selected="true"] p {
    color: white !important;
}

/* COLUNAS MAIS JUSTAS */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 2px !important;
}

div[data-testid="column"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* BLOCOS */
.bloco-azul {
    background: linear-gradient(135deg, #eaf2fb 0%, #d7e7f5 100%);
    color: #002f5f;
    padding: 28px;
    border-radius: 22px;
    margin: 14px 0 28px 0;
    border-left: 8px solid #002f5f;
    border-top: 1px solid #c9d9ea;
    border-right: 1px solid #c9d9ea;
    border-bottom: 1px solid #c9d9ea;
}

.foco-final {
    font-size: 34px;
    font-weight: 850;
    line-height: 1.3;
}

.info-equipe {
    font-size: 22px;
    line-height: 1.7;
}

/* EXPLICAÇÕES */
.step-card {
    background: linear-gradient(135deg, #eaf2fb 0%, #d7e7f5 100%);
    padding: 24px;
    border-radius: 22px;
    border-left: 8px solid #002f5f;
    border-top: 1px solid #c9d9ea;
    border-right: 1px solid #c9d9ea;
    border-bottom: 1px solid #c9d9ea;
    margin-bottom: 24px;
}

.step-title {
    color: #002f5f;
    font-size: 27px;
    font-weight: 850;
    margin-bottom: 8px;
}

.step-help {
    color: #24476b;
    font-size: 19px;
    margin-bottom: 0;
}

/* CAMPOS */
div[data-testid="stTextInput"] input {
    font-size: 24px;
    height: 66px;
    border-radius: 18px;
    border: 2px solid #cfd9e6;
    background-color: #ffffff;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #6b7280 !important;
}

textarea {
    font-size: 22px !important;
    border-radius: 18px !important;
    border: 2px solid #cfd9e6 !important;
    color: #111827 !important;
    background-color: #ffffff !important;
}

textarea::placeholder {
    color: #6b7280 !important;
}

.stNumberInput input {
    font-size: 22px;
    height: 60px;
    border-radius: 16px;
    color: #111827 !important;
    background-color: #ffffff !important;
}

/* BOTÕES */
.stButton > button {
    width: 100%;
    min-height: 58px;
    border-radius: 16px;
    border: 2px solid #002f5f;
    background: #002f5f;
    color: white;
    font-weight: 800;
    font-size: 18px;
    padding-left: 8px;
    padding-right: 8px;
}

.stButton > button:hover {
    background: #00447f;
    border-color: #00447f;
    color: white;
}

/* POST-ITS */
.postit {
    background: #fff6b8;
    padding: 26px;
    border-radius: 22px;
    min-height: 190px;
    margin-bottom: 20px;
    color: #1f2937;
    border: 2px solid #f0dc7a;
}

.postit-votado {
    background: #d9fbe3;
    padding: 26px;
    border-radius: 22px;
    min-height: 190px;
    margin-bottom: 20px;
    color: #1f2937;
    border: 3px solid #16a34a;
}

.postit h4,
.postit-votado h4 {
    color: #002f5f;
    font-size: 22px;
    margin-top: 0;
    margin-bottom: 14px;
    font-weight: 850;
}

.postit-texto {
    color: #111827;
    font-size: 25px;
    line-height: 1.45;
    font-weight: 800;
}

.votos {
    color: #002f5f;
    font-size: 20px;
    font-weight: 850;
    margin-top: 18px;
}

/* CELULAR */
@media (max-width: 768px) {

    .main .block-container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        padding-top: 1rem;
    }

    h1 {
        font-size: 34px !important;
    }

    h2 {
        font-size: 29px !important;
    }

    h3 {
        font-size: 25px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 70px;
        padding: 0 12px;
        border-radius: 18px;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 20px !important;
        line-height: 1.05 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 2px !important;
    }

    .stButton > button {
        min-height: 54px;
        font-size: 16px;
        border-radius: 14px;
        padding-left: 4px;
        padding-right: 4px;
    }

    .step-card {
        padding: 20px;
        border-radius: 20px;
        border-left: 7px solid #002f5f;
    }

    .step-title {
        font-size: 25px;
    }

    .step-help {
        font-size: 19px;
    }

    div[data-testid="stTextInput"] input,
    textarea,
    .stNumberInput input {
        font-size: 22px !important;
    }

    .postit-texto {
        font-size: 25px;
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
        if st.button("Iniciar", key=f"iniciar_{nome_timer}"):
            st.session_state[nome_timer] = time.time()

    with col2:
        if st.button("Parar", key=f"encerrar_{nome_timer}"):
            st.session_state[nome_timer] = None
            st.warning("Cronômetro parado.")

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
# FOCO GERAL
# =========================

st.markdown(
    """
    <h2 style="text-align:center; color:#002f5f;">
        Foco
    </h2>
    """,
    unsafe_allow_html=True
)

if st.session_state.editando_foco:

    foco_digitado = st.text_input(
        label="campo_foco",
        value=st.session_state.foco_salvo,
        placeholder="Digite o tema da reunião",
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
# ABAS
# =========================

aba1, aba2 = st.tabs([
    "Foco no Foco",
    "Principais Obstáculos"
])


# =========================
# ABA 1
# =========================

with aba1:

    st.title("Foco no Foco")

    st.markdown(
        """
<div class="step-card">
<div class="step-title">1. Informe sua equipe</div>
<div class="step-help">Digite o nome da equipe e o líder. Depois clique em salvar.</div>
</div>
""",
        unsafe_allow_html=True
    )

    if "nome_equipe_salvo" not in st.session_state:
        st.session_state.nome_equipe_salvo = ""

    if "lider_equipe_salvo" not in st.session_state:
        st.session_state.lider_equipe_salvo = ""

    if "editando_equipe" not in st.session_state:
        st.session_state.editando_equipe = True

    tempo_cadastro_minutos = st.number_input(
        "Tempo para essa etapa em minutos",
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
            placeholder="Exemplo: Time Azul"
        )

        lider_equipe_digitado = st.text_input(
            "Líder da equipe",
            value=st.session_state.lider_equipe_salvo,
            placeholder="Exemplo: Ana"
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

    st.markdown(
        """
<div class="step-card">
<div class="step-title">2. Escreva seu post-it</div>
<div class="step-help">Escreva uma frase com exatamente 6 palavras. Depois clique em adicionar.</div>
</div>
""",
        unsafe_allow_html=True
    )

    tempo_postit_minutos = st.number_input(
        "Tempo para escrever os post-its em minutos",
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
        placeholder="Exemplo: Melhorar comunicação entre áreas internas críticas"
    )

    qtd_palavras = contar_palavras(novo_postit)

    st.caption(f"{qtd_palavras}/6 palavras")

    if qtd_palavras < 6 and qtd_palavras > 0:
        st.warning("Faltam palavras. O post-it precisa ter exatamente 6.")

    if qtd_palavras > 6:
        st.error("Tem palavras demais. O post-it precisa ter exatamente 6.")

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

    st.markdown(
        """
<div class="step-card">
<div class="step-title">3. Vote nos post-its</div>
<div class="step-help">Leia os post-its e clique em votar. Se errar, clique em desfazer voto.</div>
</div>
""",
        unsafe_allow_html=True
    )

    cursor.execute("""
    SELECT id, equipe, texto, votos
    FROM postits
    WHERE ativo = 1
    ORDER BY id DESC
    """)

    postits = cursor.fetchall()

    if postits:

        for postit_id, equipe, texto, votos in postits:

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
        st.info("Nenhum post-it disponível ainda.")

    st.markdown(
        """
<div class="step-card">
<div class="step-title">4. Veja o resultado</div>
<div class="step-help">O post-it mais votado aparece abaixo. Se empatar, faça uma nova votação apenas com os empatados.</div>
</div>
""",
        unsafe_allow_html=True
    )

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
            "Houve empate. Faça uma nova votação apenas com os empatados."
        )

        if st.button("Iniciar votação de desempate"):

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
        st.info("O resultado aparecerá aqui após a votação.")

    col_reset1, col_reset2 = st.columns(
    [1,1],
    gap="small"
    )

    st.markdown("""
    <style>
    div[data-testid="column"] {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with col_reset1:
        if st.button("Zerar votos"):
            cursor.execute("UPDATE postits SET votos = 0")
            conn.commit()
            st.session_state.postits_votados = set()
            st.rerun()

    with col_reset2:
        if st.button("Mostrar todos"):
            cursor.execute("UPDATE postits SET ativo = 1")
            conn.commit()
            st.session_state.postits_votados = set()
            st.rerun()


# =========================
# ABA 2
# =========================

with aba2:

    st.title("Principais Obstáculos")

    st.info("Essa aba está reservada para a próxima etapa.")
