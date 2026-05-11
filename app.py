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
    color: rgba(255,255,255,0.85);
    font-size: 28px;
    font-weight: 600;
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
        font-size: 22px;
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
    ativo INTEGER DEFAULT 1,
    sala TEXT DEFAULT 'geral'
)
""")
conn.commit()

try:
    cursor.execute("ALTER TABLE postits ADD COLUMN sala TEXT DEFAULT 'geral'")
    conn.commit()
except:
    pass

cursor.execute("""
CREATE TABLE IF NOT EXISTS salas (
    sala TEXT PRIMARY KEY,
    foco TEXT
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS entraves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sala TEXT,
    equipe TEXT,
    texto TEXT,
    votos INTEGER DEFAULT 0
)
""")
conn.commit()

try:
    cursor.execute("ALTER TABLE entraves ADD COLUMN votos INTEGER DEFAULT 0")
    conn.commit()
except:
    pass

cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias_entraves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sala TEXT,
    categoria TEXT,
    entrave_id INTEGER
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


def buscar_mais_votados(sala_atual):

    cursor.execute("""
    SELECT id, equipe, texto, votos
    FROM postits
    WHERE ativo = 1 AND sala = ?
    ORDER BY votos DESC
    """, (sala_atual,))

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

if "sala" not in st.session_state:
    st.session_state.sala = None

if "postits_votados" not in st.session_state:
    st.session_state.postits_votados = set()

if "foco_salvo" not in st.session_state:
    st.session_state.foco_salvo = ""

if "editando_foco" not in st.session_state:
    st.session_state.editando_foco = True


# =========================
# ENTRADA POR SENHA / SALA
# =========================

# =========================
# ENTRADA POR SENHA / SALA
# =========================

if st.session_state.sala is None:

    st.markdown(
        """
<div style="
    text-align:center;
    margin-bottom:18px;
">

<div style="
    color:#002f5f;
    font-size:18px;
    font-weight:700;
    letter-spacing:6px;
    text-transform:uppercase;
    opacity:0.75;
    margin-bottom:8px;
">
EMBRAER
</div>

<div style="
    color:#002f5f;
    font-size:56px;
    font-weight:900;
    line-height:1;
    margin-bottom:10px;
">
SIX SIMPLIFY
</div>

<div style="
    color:#4b6584;
    font-size:24px;
    font-weight:600;
    letter-spacing:2px;
    text-transform:uppercase;
">
Workshop
</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="header-foco">
<div class="header-title">Entrar na sala</div>
<div class="header-subtitle">Digite a senha combinada para acessar a dinâmica</div>
</div>
""",
        unsafe_allow_html=True
    )

    senha_sala = st.text_input(
        "Senha da sala",
        type="password",
        placeholder="Digite a senha da reunião"
    )

    if st.button("Entrar"):
        if senha_sala.strip():
            st.session_state.sala = senha_sala.strip()
            st.session_state.postits_votados = set()
            st.rerun()
        else:
            st.warning("Digite uma senha para entrar.")

    st.stop()

sala_atual = st.session_state.sala

cursor.execute(
    "SELECT foco FROM salas WHERE sala = ?",
    (sala_atual,)
)
foco_banco = cursor.fetchone()

if foco_banco:
    st.session_state.foco_salvo = foco_banco[0]
else:
    st.session_state.foco_salvo = ""


# =========================
# FOCO GERAL
# =========================

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


# =========================
# ABAS
# =========================

aba0, aba1, aba2 = st.tabs([
    "Summary",
    "Foco no Foco",
    "Principais Entraves"
])

# =========================
# ABA 0
# =========================

# =========================
# ABA 0 - SUMMARY
# =========================

with aba0:

    st.title("Summary")

    st.markdown(
        """
<div class="step-card">
<div class="step-title">Resumo do workshop</div>
<div class="step-help">Aqui aparecem os principais resultados consolidados das próximas abas.</div>
</div>
""",
        unsafe_allow_html=True
    )

    # =========================
    # FOCO
    # =========================

    st.markdown("## Foco")

    if st.session_state.foco_salvo:

        st.markdown(
            f"""
<div class="resultado-final-header">
<div class="resultado-label">FOCO DA REUNIÃO</div>
<div class="resultado-texto">{st.session_state.foco_salvo}</div>
</div>
""",
            unsafe_allow_html=True
        )

    else:
        st.info("O foco da reunião ainda não foi definido.")

    # =========================
    # FOCO NO FOCO
    # =========================

    st.markdown("## Foco no Foco")

    vencedores_summary, maior_voto_summary, tem_empate_summary = buscar_mais_votados(
        sala_atual
    )

    if vencedores_summary and not tem_empate_summary:

        st.markdown(
            f"""
<div class="resultado-final-header">
<div class="resultado-label">FOCO NO FOCO</div>
<div class="resultado-texto">{vencedores_summary[0][2]}</div>
</div>
""",
            unsafe_allow_html=True
        )

    elif tem_empate_summary:

        st.warning(
            "Há empate no Foco no Foco. Faça a votação de desempate na aba Foco no Foco."
        )

    else:

        st.info("O Foco no Foco ainda não foi definido pela votação.")

    # =========================
    # ENTRAVES POR CATEGORIA
    # =========================

    st.markdown("## Entraves categorizados")

    cursor.execute("""
    SELECT 
        c.categoria,
        e.equipe,
        e.texto,
        e.votos
    FROM categorias_entraves c
    JOIN entraves e ON c.entrave_id = e.id
    WHERE c.sala = ?
    ORDER BY c.categoria, e.votos DESC
    """, (sala_atual,))

    categorias_summary = cursor.fetchall()

    if categorias_summary:

        categorias_dict_summary = {}

        for categoria, equipe_cat, texto_cat, votos_cat in categorias_summary:

            if categoria not in categorias_dict_summary:
                categorias_dict_summary[categoria] = []

            categorias_dict_summary[categoria].append(
                (equipe_cat, texto_cat, votos_cat)
            )

        for categoria, itens_categoria in categorias_dict_summary.items():

            st.markdown(
                f"""
<div class="resultado-final-header">
<div class="resultado-label">CATEGORIA</div>
<div class="resultado-texto">{categoria}</div>
</div>
""",
                unsafe_allow_html=True
            )

            for equipe_cat, texto_cat, votos_cat in itens_categoria:

                st.markdown(
                    f"""
<div style="
    background:#eaf2fb;
    padding:24px;
    border-radius:22px;
    margin-bottom:14px;
    border:2px solid #c9d9ea;
    border-left:8px solid #002f5f;
">
<div style="
    color:#002f5f;
    font-size:17px;
    font-weight:900;
    margin-bottom:8px;
">
Equipe: {equipe_cat} • {votos_cat} voto(s)
</div>

<div style="
    color:#111827;
    font-size:22px;
    line-height:1.45;
    font-weight:800;
">
{texto_cat}
</div>
</div>
""",
                    unsafe_allow_html=True
                )

    else:

        st.info("Nenhum entrave foi categorizado ainda.")
        
# =========================
# ABA 1
# =========================

with aba1:

    st.title("Foco no Foco")

    st.caption(f"Sala atual: {sala_atual}")

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

        if not nome_equipe.strip():
            st.warning("Salve o nome da equipe antes de adicionar um post-it.")
        elif qtd_palavras != 6:
            st.error("O post-it precisa ter exatamente 6 palavras.")
        else:
            cursor.execute("""
            INSERT INTO postits (equipe, texto, votos, ativo, sala)
            VALUES (?, ?, 0, 1, ?)
            """, (nome_equipe, novo_postit, sala_atual))

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
    WHERE ativo = 1 AND sala = ?
    ORDER BY id DESC
    """, (sala_atual,))

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
                    WHERE id = ? AND sala = ?
                    """, (postit_id, sala_atual))

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
                    WHERE id = ? AND sala = ?
                    """, (postit_id, sala_atual))

                    conn.commit()
                    st.session_state.postits_votados.add(postit_id)
                    st.rerun()

    else:
        st.info("Nenhum post-it disponível ainda nesta sala.")

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

    vencedores, maior_voto, tem_empate = buscar_mais_votados(sala_atual)

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

            cursor.execute(
                "UPDATE postits SET ativo = 0 WHERE sala = ?",
                (sala_atual,)
            )

            cursor.execute(
                f"""
                UPDATE postits
                SET ativo = 1, votos = 0
                WHERE id IN ({",".join(ids_empatados)}) AND sala = ?
                """,
                (sala_atual,)
            )

            conn.commit()
            st.session_state.postits_votados = set()
            st.rerun()

    else:
        st.info("O resultado aparecerá aqui após a votação.")

    if st.button("Mostrar todos"):
        cursor.execute(
            "UPDATE postits SET ativo = 1 WHERE sala = ?",
            (sala_atual,)
        )
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()

    if st.button("Zerar votos"):
        cursor.execute(
            "UPDATE postits SET votos = 0 WHERE sala = ?",
            (sala_atual,)
        )
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()

# =========================
# ABA 2
# =========================

with aba2:

    st.title("Principais Entraves")

    st.markdown(
        """
<div class="step-card">
<div class="step-title">Adicionar entrave</div>
<div class="step-help">Cada equipe pode adicionar quantos post-its quiser. Todos os participantes da mesma sala conseguirão visualizar e votar no mural completo.</div>
</div>
""",
        unsafe_allow_html=True
    )

    tempo_entraves_minutos = st.number_input(
        "Tempo para pensar nos entraves em minutos",
        min_value=1,
        max_value=60,
        value=7,
        key="tempo_entraves"
    )

    mostrar_cronometro(
        "timer_entraves",
        int(tempo_entraves_minutos * 60)
    )

    equipe_entrave = st.session_state.nome_equipe_salvo

    novo_entrave = st.text_area(
        "Novo post-it de entrave",
        placeholder="Digite aqui o principal entrave identificado pela equipe",
        key="campo_entrave"
    )

    if st.button("Adicionar entrave", key="botao_adicionar_entrave"):

        if not equipe_entrave.strip():
            st.warning("Salve o nome da equipe na aba Foco no Foco antes de adicionar entraves.")

        elif not novo_entrave.strip():
            st.warning("Digite o texto do entrave antes de adicionar.")

        else:
            cursor.execute("""
            INSERT INTO entraves (sala, equipe, texto, votos)
            VALUES (?, ?, ?, 0)
            """, (
                sala_atual,
                equipe_entrave,
                novo_entrave.strip()
            ))

            conn.commit()
            st.success("Entrave adicionado!")
            st.rerun()

    st.markdown("## Mural de entraves por equipe")

    cursor.execute("""
    SELECT id, equipe, texto, votos
    FROM entraves
    WHERE sala = ?
    ORDER BY equipe, id
    """, (sala_atual,))

    entraves = cursor.fetchall()

    cores_times = [
        "#fff6b8",
        "#ffd6a5",
        "#caffbf",
        "#bde0fe",
        "#ffc8dd",
        "#d0bfff",
        "#fdffb6",
        "#a0c4ff",
        "#e2ece9",
        "#f1c0e8",
    ]

    if "entraves_votados" not in st.session_state:
        st.session_state.entraves_votados = set()

    rankings = []

    if entraves:

        equipes = {}

        for entrave_id, equipe, texto, votos in entraves:

            if equipe not in equipes:
                equipes[equipe] = []

            equipes[equipe].append(
                (entrave_id, texto, votos)
            )

        for indice, (equipe, lista_entraves) in enumerate(equipes.items()):

            cor_time = cores_times[indice % len(cores_times)]

            st.markdown(
                f"""
<div style="
    background:#ffffff;
    border:2px solid #d7e7f5;
    border-left:10px solid #002f5f;
    border-radius:28px;
    padding:28px;
    margin:32px 0;
    box-shadow:0 8px 24px rgba(15,23,42,0.06);
">
<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    margin-bottom:22px;
    border-bottom:2px solid #e5eef7;
    padding-bottom:18px;
">
<div>
<div style="
    color:#002f5f;
    font-size:30px;
    font-weight:900;
    line-height:1.1;
">
{equipe}
</div>
<div style="
    color:#55708f;
    font-size:17px;
    font-weight:600;
    margin-top:6px;
">
Mural de entraves da equipe
</div>
</div>
<div style="
    background:{cor_time};
    color:#002f5f;
    border:2px solid rgba(0,47,95,0.15);
    padding:10px 16px;
    border-radius:999px;
    font-size:16px;
    font-weight:800;
">
{len(lista_entraves)} post-it(s)
</div>
</div>
</div>
""",
                unsafe_allow_html=True
            )

            colunas_mural = st.columns(1)

            for i, (entrave_id, texto, votos) in enumerate(lista_entraves):

                with colunas_mural[0]:

                    foi_votado = entrave_id in st.session_state.entraves_votados

                    cor_postit = "#fbcfe8" if foi_votado else cor_time
                    borda = "3px solid #ec4899" if foi_votado else "2px solid rgba(0,47,95,0.18)"

                    html_postit = f"""
<div style="
    background:{cor_postit};
    padding:24px;
    border-radius:22px;
    min-height:130px;
    margin-bottom:14px;
    color:#111827;
    border:{borda};
    box-shadow:0 6px 16px rgba(15,23,42,0.08);
">
<div style="
    color:#111827;
    font-size:23px;
    line-height:1.45;
    font-weight:800;
">
{texto}
</div>
<div style="
    margin-top:16px;
    color:#002f5f;
    font-size:18px;
    font-weight:800;
">
Votos: {votos}
</div>
</div>
"""

                    st.markdown(html_postit, unsafe_allow_html=True)

                    if foi_votado:

                        if st.button(
                            "Desfazer voto",
                            key=f"desfazer_entrave_{entrave_id}"
                        ):
                            cursor.execute("""
                            UPDATE entraves
                            SET votos = CASE
                                WHEN votos > 0 THEN votos - 1
                                ELSE 0
                            END
                            WHERE id = ?
                            AND sala = ?
                            """, (
                                entrave_id,
                                sala_atual
                            ))

                            conn.commit()
                            st.session_state.entraves_votados.remove(entrave_id)
                            st.rerun()

                    else:

                        if st.button(
                            "Votar",
                            key=f"votar_entrave_{entrave_id}"
                        ):
                            cursor.execute("""
                            UPDATE entraves
                            SET votos = votos + 1
                            WHERE id = ?
                            AND sala = ?
                            """, (
                                entrave_id,
                                sala_atual
                            ))

                            conn.commit()
                            st.session_state.entraves_votados.add(entrave_id)
                            st.rerun()

        st.markdown("## Ranking dos entraves mais votados")

        cursor.execute("""
        SELECT equipe, texto, votos, id
        FROM entraves
        WHERE sala = ?
        AND votos > 0
        ORDER BY votos DESC, id ASC
        """, (sala_atual,))

        entraves_mais_votados = cursor.fetchall()

        if entraves_mais_votados:

            votos_ja_usados = []

            for item in entraves_mais_votados:
                votos_item = item[2]

                if votos_item not in votos_ja_usados:
                    votos_ja_usados.append(votos_item)

                posicao = votos_ja_usados.index(votos_item) + 1

                if posicao <= 3:
                    rankings.append((posicao, item))

            st.markdown(
                """
<div class="resultado-final-header">
<div class="resultado-label">RANKING DOS ENTRAVES</div>
<div class="resultado-texto">Top 3 mais votados</div>
</div>
""",
                unsafe_allow_html=True
            )

            for posicao, (equipe_top, texto_top, votos_top, entrave_id_top) in rankings:

                if posicao == 1:
                    titulo_ranking = "1º lugar"
                    cor_ranking = "#e79eff"
                    borda_ranking = "#8f7193"
                elif posicao == 2:
                    titulo_ranking = "2º lugar"
                    cor_ranking = "#dbeafe"
                    borda_ranking = "#2563eb"
                else:
                    titulo_ranking = "3º lugar"
                    cor_ranking = "#c7f7f7"
                    borda_ranking = "#96c4c4"

                st.markdown(
                    f"""
<div style="
    background:{cor_ranking};
    padding:26px;
    border-radius:22px;
    min-height:130px;
    margin-bottom:16px;
    color:#111827;
    border:3px solid {borda_ranking};
    box-shadow:0 6px 16px rgba(15,23,42,0.08);
">
<div style="
    color:#002f5f;
    font-size:20px;
    font-weight:900;
    margin-bottom:8px;
">
{titulo_ranking} • {votos_top} voto(s)
</div>
<div style="
    color:#002f5f;
    font-size:17px;
    font-weight:800;
    margin-bottom:10px;
">
Equipe: {equipe_top}
</div>
<div style="
    color:#111827;
    font-size:24px;
    line-height:1.45;
    font-weight:850;
">
{texto_top}
</div>
</div>
""",
                    unsafe_allow_html=True
                )

        else:
            st.info("O ranking dos entraves aparecerá aqui após a votação.")

    else:
        st.info("Nenhum entrave adicionado ainda nesta sala.")

    st.markdown("## Categorizar entraves do Top 3")

    if "limpar_categoria" not in st.session_state:
        st.session_state["limpar_categoria"] = False

    if st.session_state["limpar_categoria"]:
        st.session_state["nova_categoria_entraves"] = ""
        st.session_state["entraves_para_categoria"] = []
        st.session_state["limpar_categoria"] = False

    if rankings:

        opcoes_top3 = {
            f"{posicao}º lugar | {item[0]} | {item[1]}": item
            for posicao, item in rankings
        }

        nova_categoria = st.text_input(
            "Nome da categoria",
            placeholder="Exemplo: Tecnologia",
            key="nova_categoria_entraves"
        )

        entraves_escolhidos = st.multiselect(
            "Escolha os entraves",
            options=list(opcoes_top3.keys()),
            key="entraves_para_categoria"
        )

        if st.button("Salvar categoria"):

            if not nova_categoria.strip():
                st.warning("Digite o nome da categoria.")

            elif not entraves_escolhidos:
                st.warning("Escolha pelo menos um entrave.")

            else:

                for item_escolhido in entraves_escolhidos:

                    dados_entrave = opcoes_top3[item_escolhido]
                    entrave_id_top = dados_entrave[3]

                    cursor.execute("""
                    INSERT INTO categorias_entraves (
                        sala,
                        categoria,
                        entrave_id
                    )
                    VALUES (?, ?, ?)
                    """, (
                        sala_atual,
                        nova_categoria.strip(),
                        entrave_id_top
                    ))

                conn.commit()

                st.session_state["limpar_categoria"] = True

                st.success("Categoria criada!")
                st.rerun()

    else:
        st.info("A categorização aparecerá após existirem entraves no Top 3.")

    st.markdown("## Categorias criadas")

    cursor.execute("""
    SELECT 
        c.id,
        c.categoria,
        e.equipe,
        e.texto,
        e.votos
    FROM categorias_entraves c
    JOIN entraves e ON c.entrave_id = e.id
    WHERE c.sala = ?
    ORDER BY c.categoria, e.votos DESC
    """, (sala_atual,))

    categorias_salvas = cursor.fetchall()

    if categorias_salvas:

        categorias_dict = {}

        for row_id, categoria, equipe_cat, texto_cat, votos_cat in categorias_salvas:

            if categoria not in categorias_dict:
                categorias_dict[categoria] = []

            categorias_dict[categoria].append(
                (
                    row_id,
                    equipe_cat,
                    texto_cat,
                    votos_cat
                )
            )

        for categoria, itens_categoria in categorias_dict.items():

            st.markdown(
                f"""
<div class="resultado-final-header">
<div class="resultado-label">CATEGORIA</div>
<div class="resultado-texto">{categoria}</div>
</div>
""",
                unsafe_allow_html=True
            )

            for item_categoria in itens_categoria:

                categoria_id = item_categoria[0]
                equipe_cat = item_categoria[1]
                texto_cat = item_categoria[2]
                votos_cat = item_categoria[3]

                col_categoria1, col_categoria2 = st.columns([9, 1])

                with col_categoria1:

                    st.markdown(
                        f"""
<div style="
    background:#eaf2fb;
    padding:24px;
    border-radius:22px;
    margin-bottom:14px;
    border:2px solid #c9d9ea;
    border-left:8px solid #002f5f;
">
<div style="
    color:#002f5f;
    font-size:17px;
    font-weight:900;
    margin-bottom:8px;
">
Equipe: {equipe_cat} • {votos_cat} voto(s)
</div>
<div style="
    color:#111827;
    font-size:22px;
    line-height:1.45;
    font-weight:800;
">
{texto_cat}
</div>
</div>
""",
                        unsafe_allow_html=True
                    )

                with col_categoria2:

                    if st.button(
                        "✕",
                        key=f"remover_categoria_{categoria_id}"
                    ):

                        cursor.execute("""
                        DELETE FROM categorias_entraves
                        WHERE id = ?
                        """, (categoria_id,))

                        conn.commit()
                        st.rerun()

    else:
        st.info("Nenhuma categoria criada ainda.")
