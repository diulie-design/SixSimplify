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

/* HEADER FOCO */
.header-foco {
    background: linear-gradient(135deg, #002f5f 0%, #0a4d8c 100%);
    padding: 36px 28px;
    border-radius: 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(0,47,95,0.15);
}



.header-title {
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: 850;
    line-height: 1.1;
    margin-bottom: 8px;
}

.header-subtitle {
    text-align: center;
    color: rgba(255,255,255,0.75);
    font-size: 34px;
    font-weight: 500;
}

.foco-salvo-card {
    background: linear-gradient(135deg, #eaf2fb 0%, #d7e7f5 100%);
    color: #002f5f;
    padding: 28px;
    border-radius: 22px;
    margin: 14px 0 28px 0;
    border-left: 8px solid #002f5f;
    border-top: 1px solid #c9d9ea;
    border-right: 1px solid #c9d9ea;
    border-bottom: 1px solid #c9d9ea;
    font-size: 34px;
    font-weight: 850;
    line-height: 1.3;
    text-align: center;
}

.resultado-final-header {
    background: linear-gradient(135deg, #0b3b6e 0%, #14508f 100%);
    padding: 34px 28px;
    border-radius: 28px;
    margin-top: 18px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,47,95,0.18);
    text-align: center;
}

.resultado-label {
    color: rgba(255,255,255,0.75);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.resultado-texto {
    color: white;
    font-size: 38px;
    font-weight: 850;
    line-height: 1.25;
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

/* COLUNAS */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 0px !important;
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
    text-align: center;
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
    font-size: 22px;
    line-height: 1.4;
    padding-top: 10px;
    padding-bottom: 10px;
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
    margin: 0 !important;
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

    .header-foco {
        padding: 28px 20px;
        border-radius: 24px;
    }

    .header-title {
        font-size: 36px;
    }

    .header-subtitle {
        font-size: 17px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
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
        gap: 0px !important;
    }

    div[data-testid="column"] {
        padding-left: 0px !important;
        padding-right: 0px !important;
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    .stButton > button {
        width: 100% !important;
        margin: 0px !important;
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

    div[data-testid="stTextInput"] input {
        font-size: 21px !important;
        line-height: 1.4 !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }

    textarea,
    .stNumberInput input {
        font-size: 21px !important;
    }

    .postit-texto {
        font-size: 25px;
    }
}



/* TOPO FIXO NO CELULAR */
.espaco-topo-fixo-mobile {
    display: none;
}

@media (max-width: 768px) {

    .st-key-topo_fixo_mobile {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 9999 !important;
        background: #f7f9fc !important;
        padding: 8px 12px 10px 12px !important;
        box-shadow: 0 8px 24px rgba(15,23,42,0.12) !important;
    }

    .st-key-topo_fixo_mobile .header-foco {
        margin: 0 0 8px 0 !important;
        padding: 16px 12px !important;
        border-radius: 18px !important;
    }

    .st-key-topo_fixo_mobile .header-title {
        font-size: 28px !important;
        line-height: 1.05 !important;
        margin-bottom: 4px !important;
    }

    .st-key-topo_fixo_mobile .header-subtitle {
        font-size: 18px !important;
        line-height: 1.15 !important;
    }

    .st-key-topo_fixo_mobile div[data-testid="stTextInput"] input {
        min-height: 48px !important;
        font-size: 18px !important;
        border-radius: 14px !important;
    }

    .st-key-topo_fixo_mobile .stButton > button {
        min-height: 44px !important;
        font-size: 15px !important;
        border-radius: 14px !important;
        margin-top: 4px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        position: fixed !important;
        top: 230px !important;
        left: 12px !important;
        right: 12px !important;
        z-index: 9998 !important;
        background: #f7f9fc !important;
        padding: 8px 0 8px 0 !important;
        margin-bottom: 0 !important;
        border-bottom: 2px solid #e5eef7 !important;
        box-shadow: 0 6px 14px rgba(15,23,42,0.06) !important;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 58px !important;
        padding: 0 10px !important;
        border-radius: 16px !important;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 17px !important;
    }

    .espaco-topo-fixo-mobile {
        display: block !important;
        height: 310px !important;
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

    if st.session_state[nome_timer] is None:

        if st.button(
            "Iniciar cronômetro",
            key=f"iniciar_{nome_timer}"
        ):
            st.session_state[nome_timer] = time.time()
            st.rerun()

    else:

        if st.button(
            "Parar cronômetro",
            key=f"parar_{nome_timer}"
        ):
            st.session_state[nome_timer] = None
            st.rerun()

    if st.session_state[nome_timer]:

        st_autorefresh(
            interval=1000,
            key=f"refresh_{nome_timer}"
        )

        tempo_passado = int(
            time.time() - st.session_state[nome_timer]
        )

        tempo_restante = max(
            tempo_total_segundos - tempo_passado,
            0
        )

        minutos = tempo_restante // 60
        segundos = tempo_restante % 60

        st.markdown(
            f"## ⏱️ {minutos:02d}:{segundos:02d}"
        )

        st.progress(
            tempo_restante / tempo_total_segundos
        )

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

with st.container(key="topo_fixo_mobile"):

    tema_header = (
        st.session_state.foco_salvo
        if st.session_state.foco_salvo
        else "Defina o tema principal da reunião"
    )

    st.markdown(
        f"""
<div class="header-foco">
<div class="header-title">Foco</div>
<div class="header-subtitle">{tema_header}</div>
</div>
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

                cursor.execute("""
                INSERT INTO salas (sala, foco)
                VALUES (?, ?)
                ON CONFLICT(sala) DO UPDATE SET foco = excluded.foco
                """, (sala_atual, st.session_state.foco_salvo))

                conn.commit()

                st.session_state.editando_foco = False
                st.rerun()
            else:
                st.warning("Digite um foco antes de salvar.")

    else:

        if st.button("Editar foco"):
            st.session_state.editando_foco = True
            st.rerun()

st.markdown(
    '<div class="espaco-topo-fixo-mobile"></div>',
    unsafe_allow_html=True
)

# =========================
# ABAS
# =========================

aba1, aba2 = st.tabs([
    "Foco no Foco",
    "Principais Entraves"
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
<div class="resultado-final-header">
<div class="resultado-label">FOCO NO FOCO</div>
<div class="resultado-texto">{vencedores[0][2]}</div>
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

    if st.button("Mostrar todos"):
        cursor.execute("UPDATE postits SET ativo = 1")
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()

    if st.button("Zerar votos"):
        cursor.execute("UPDATE postits SET votos = 0")
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()


# =========================
# ABA 2
# =========================

with aba2:

    st.title("Principais Entraves")

    st.info("Essa aba está reservada para a próxima etapa.")
