import streamlit as st
import time
import sqlite3
import html
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Six Simplify Workshop", layout="wide")

# Detecta dispositivo mobile
user_agent = st.context.headers.get("User-Agent", "")
st.session_state["is_mobile"] = any(
    termo in user_agent.lower()
    for termo in ["iphone", "android", "mobile"]
)


# =========================
# AUTOREFRESH GLOBAL
# =========================

st_autorefresh(
    interval=5000,
    key="refresh_global"
)

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

/* HEADER */
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

/* CABEÇALHO FIXO */
.fixed-workshop-header {
    position: fixed !important;
    top: 160px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(1000px, calc(100vw - 48px)) !important;
    z-index: 2147483000 !important;
    background: rgba(247, 249, 252, 0.92) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    padding: 10px 0 10px 0 !important;
    border-radius: 32px !important;
}

.fixed-workshop-header .header-foco {
    margin-bottom: 0 !important;
}

.fixed-workshop-header-spacer {
    height: 300px;
}

.landing-title {
    text-align: center;
    margin-bottom: 18px;
}

.landing-embraer {
    color: #002f5f;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 6px;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 8px;
}

.landing-main {
    color: #002f5f;
    font-size: 56px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 10px;
}

.landing-sub {
    color: #4b6584;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
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

/* NAVEGAÇÃO COM BOTÕES FIXA */
div[role="radiogroup"] {
    position: fixed !important;
    top: 12px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(1000px, calc(100vw - 48px)) !important;
    z-index: 2147483100 !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 3px !important;
    margin-bottom: 0 !important;
    background: rgba(247, 249, 252, 0.94) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    padding: 10px !important;
    border-radius: 28px !important;
    box-shadow: 0 10px 30px rgba(15,23,42,0.10) !important;
}

div[role="radiogroup"] label {
    background: #ffffff;
    border: 2px solid #dbe4ef;
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 54px;
    color: #002f5f;
    font-weight: 800;
    flex: 1 1 auto !important;
    justify-content: flex-start !important;
    white-space: nowrap !important;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #002f5f;
    border-color: #002f5f;
    color: white;
}

div[role="radiogroup"] label p {
    font-size: 21px !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
}

div[role="radiogroup"] label:has(input:checked) p {
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
    min-height: 260px;
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

/* CRONÔMETRO COMPARTILHADO */
.timer-card {
    background: #ffffff;
    border: 2px solid #d7e7f5;
    border-left: 8px solid #002f5f;
    border-radius: 24px;
    padding: 16px 18px;
    margin: 18px 0 14px 0;
    box-shadow: 0 8px 24px rgba(15,23,42,0.06);
}

.timer-title {
    color: #002f5f;
    font-size: 22px;
    font-weight: 850;
    margin-bottom: 6px;
}

.timer-help {
    color: #55708f;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 0;
}

.timer-display {
    color: #002f5f;
    font-size: 46px;
    font-weight: 900;
    line-height: 1;
    text-align: center;
    margin-top: 10px;
}

.timer-status {
    color: #24476b;
    font-size: 16px;
    font-weight: 700;
    text-align: center;
    margin-top: 6px;
}

/* BOTÃO DO RELÓGIO DO CRONÔMETRO */
.st-key-timer_area_foco_no_foco .stButton > button,
.st-key-timer_area_principais_entraves .stButton > button {
    min-height: 104px !important;
    height: 104px !important;
    width: 104px !important;
    border-radius: 999px !important;
    font-size: 46px !important;
    line-height: 1 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-shadow: 0 10px 24px rgba(0,47,95,0.22) !important;
}

.st-key-timer_area_foco_no_foco .stButton > button p,
.st-key-timer_area_principais_entraves .stButton > button p {
    font-size: 46px !important;
    line-height: 1 !important;
}

/* PÍLULA FLUTUANTE DO TEMPO */
.timer-floating-pill {
    position: fixed;
    top: 86px;
    right: 22px;
    z-index: 999999;
    background: rgba(255, 255, 255, 0.96);
    border: 2px solid #c9d9ea;
    border-left: 8px solid #002f5f;
    border-radius: 999px;
    padding: 12px 18px 12px 16px;
    box-shadow: 0 14px 34px rgba(0,47,95,0.24);
    display: flex;
    align-items: center;
    gap: 12px;
    color: #002f5f;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.timer-floating-label {
    font-size: 14px;
    font-weight: 850;
    color: #24476b;
    line-height: 1;
    text-align: right;
}

.timer-floating-time {
    font-size: 34px;
    font-weight: 950;
    line-height: 1;
    color: #002f5f;
}

.timer-floating-icon {
    width: 48px;
    height: 48px;
    border-radius: 999px;
    background: #002f5f;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    box-shadow: 0 8px 18px rgba(0,47,95,0.22);
}


/* PÍLULA FIXA GLOBAL DO CRONÔMETRO */
.timer-fixed-pill-global {
    position: fixed !important;
    top: 195px !important;
    right: 22px !important;
    z-index: 2147483647 !important;
    background: rgba(255,255,255,0.98) !important;
    border: 2px solid #c9d9ea !important;
    border-left: 8px solid #002f5f !important;
    border-radius: 999px !important;
    padding: 12px 18px 12px 16px !important;
    box-shadow: 0 14px 34px rgba(0,47,95,0.25) !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    color: #002f5f !important;
    font-family: inherit !important;
    pointer-events: none !important;
}

.timer-fixed-pill-label {
    font-size: 14px !important;
    font-weight: 850 !important;
    color: #24476b !important;
    line-height: 1 !important;
    text-align: right !important;
    margin-bottom: 4px !important;
}

.timer-fixed-pill-time {
    font-size: 34px !important;
    font-weight: 950 !important;
    line-height: 1 !important;
    color: #002f5f !important;
}

.timer-fixed-pill-icon {
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    border-radius: 999px !important;
    background: #002f5f !important;
    color: white !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    font-size: 26px !important;
    box-shadow: 0 8px 18px rgba(0,47,95,0.22) !important;
}


/* AJUSTES DO CRONÔMETRO */
.st-key-timer_area_foco_no_foco .stButton > button,
.st-key-timer_area_principais_entraves .stButton > button {
    margin-left: -12px !important;
    margin-right: auto !important;
}

/* aproxima os botões -/+ do campo de minutos */
div[data-testid="stNumberInput"] {
    max-width: 360px !important;
}

div[data-testid="stNumberInput"] > div {
    max-width: 360px !important;
}

/* no cronômetro, deixa o campo mais compacto */
.st-key-tempo_foco_no_foco,
.st-key-tempo_principais_entraves {
    max-width: 360px !important;
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
        padding: 16px 18px !important;
        border-radius: 22px;
        min-height: auto !important;
    }

    .header-title {
        font-size: 28px !important;
        line-height: 1.05 !important;
        margin-bottom: 6px !important;
    }

    .header-subtitle {
        font-size: 16px !important;
        line-height: 1.25 !important;
    }

    .fixed-workshop-header {
        top: 160px !important;
        width: calc(100vw - 4px) !important;
        padding: 8px 0 !important;
        border-radius: 26px !important;
    }

    .fixed-workshop-header-spacer {
    height: 300px;
}

    .landing-main {
        font-size: 40px;
    }

    .landing-sub {
        font-size: 19px;
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
        font-size: 18px !important;
        line-height: 1.05 !important;
        font-weight: 800 !important;
    }

    div[role="radiogroup"] {
        top: 8px !important;
        width: calc(100vw - 4px) !important;
        gap: 6px !important;
        padding: 8px !important;
        border-radius: 22px !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }

    div[role="radiogroup"] label {
        min-height: 46px;
        padding: 9px 10px;
        border-radius: 16px;
        flex: 0 0 auto !important;
        white-space: nowrap !important;
        max-width: 100% !important;
    }

    div[role="radiogroup"] label p {
        font-size: 16px !important;
        line-height: 1.05 !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
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

    .timer-fixed-pill-global {
        top: auto !important;
        bottom: 105px !important;
        right: 10px !important;
        padding: 9px 12px !important;
        gap: 3px !important;
        max-width: calc(100vw - 4px) !important;
    }

    .timer-fixed-pill-label {
        font-size: 11px !important;
    }

    .timer-fixed-pill-time {
        font-size: 25px !important;
    }

    .timer-fixed-pill-icon {
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        font-size: 22px !important;
    }
.timer-title {
        font-size: 12px;
    }

    .timer-display {
        font-size: 24px;
    }

    .timer-status {
        font-size: 11px;
    }
    .timer-floating-pill {
        top: auto;
        bottom: 105px;
        right: 10px;
        padding: 9px 12px 9px 12px;
        gap: 8px;
        max-width: calc(100vw - 20px);
    }

    .timer-floating-label {
        font-size: 11px;
    }

    .timer-floating-time {
        font-size: 25px;
    }

    .timer-floating-icon {
        width: 40px;
        height: 40px;
        font-size: 22px;
    }

    .st-key-timer_area_foco_no_foco .stButton > button,
    .st-key-timer_area_principais_entraves .stButton > button {
        min-height: 86px !important;
        height: 86px !important;
        width: 86px !important;
        font-size: 38px !important;
    }

    .st-key-timer_area_foco_no_foco .stButton > button p,
    .st-key-timer_area_principais_entraves .stButton > button p {
        font-size: 38px !important;
    }

    /* Campo de minutos mais compacto no celular */
    div[data-testid="stNumberInput"] {
        max-width: 235px !important;
    }

    div[data-testid="stNumberInput"] > div {
        max-width: 235px !important;
    }

    .st-key-tempo_foco_no_foco,
    .st-key-tempo_principais_entraves {
        max-width: 235px !important;
    }

    /* Relógio de iniciar/parar mais para a esquerda e mais para baixo no celular */
    .st-key-timer_area_foco_no_foco .stButton > button,
    .st-key-timer_area_principais_entraves .stButton > button {
        margin-left: -58px !important;
        margin-top: 22px !important;
        margin-right: auto !important;
    }

    /* remove qualquer espaço exagerado entre campo de tempo e relógio */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    /* AJUSTE FINAL MOBILE: header compacto e relógio reposicionado */
    .fixed-workshop-header .header-foco {
        padding: 16px 18px !important;
    }

    .fixed-workshop-header .header-title {
        font-size: 28px !important;
        line-height: 1.05 !important;
        margin-bottom: 6px !important;
    }

    .fixed-workshop-header .header-subtitle {
        font-size: 16px !important;
        line-height: 1.25 !important;
    }

    .st-key-timer_area_foco_no_foco .stButton > button,
    .st-key-timer_area_principais_entraves .stButton > button {
        margin-left: -58px !important;
        margin-top: 22px !important;
    }

    /* Mantém a pílula do cronômetro acima dos ícones flutuantes do Streamlit */
    .timer-fixed-pill-global {
        bottom: 105px !important;
    }

    .timer-floating-pill {
        bottom: 105px !important;
    }

}

    

/* AJUSTE FINAL PARA 5 ABAS FIXAS */
@media (min-width: 769px) {
    .fixed-workshop-header {
        top: 160px !important;
    }

    .fixed-workshop-header-spacer {
        height: 300px !important;
    }

    .timer-fixed-pill-global {
        top: 195px !important;
    }
}

@media (max-width: 768px) {
    .fixed-workshop-header {
        top: 160px !important;
    }

    .fixed-workshop-header-spacer {
        height: 300px !important;
    }
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* =========================================================
   BOTÃO FLUTUANTE PARA MOSTRAR/ESCONDER CABEÇALHO FIXO
   ========================================================= */

.st-key-toggle_cabecalho_fixo {
    position: fixed !important;
    top: 16px !important;
    right: 18px !important;
    z-index: 2147483647 !important;
}

.st-key-toggle_cabecalho_fixo .stButton > button {
    width: auto !important;
    min-width: 132px !important;
    min-height: 44px !important;
    height: 44px !important;
    padding: 0 14px !important;
    border-radius: 999px !important;
    font-size: 14px !important;
    font-weight: 850 !important;
    background: #002f5f !important;
    color: white !important;
    border: 2px solid #002f5f !important;
    box-shadow: 0 8px 22px rgba(0,47,95,0.22) !important;
}

.st-key-toggle_cabecalho_fixo .stButton > button:hover {
    background: #00447f !important;
    border-color: #00447f !important;
    color: white !important;
}

@media (max-width: 768px) {
    .st-key-toggle_cabecalho_fixo {
        top: auto !important;
        right: 10px !important;
        bottom: 24px !important;
    }

    .st-key-toggle_cabecalho_fixo .stButton > button {
        min-width: 92px !important;
        min-height: 42px !important;
        height: 42px !important;
        padding: 0 11px !important;
        font-size: 12px !important;
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
except Exception:
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
except Exception:
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


cursor.execute("""
CREATE TABLE IF NOT EXISTS timers (
    sala TEXT,
    aba TEXT,
    inicio REAL,
    duracao INTEGER,
    ativo INTEGER DEFAULT 0,
    PRIMARY KEY (sala, aba)
)
""")
conn.commit()


# =========================
# FUNÇÕES
# =========================

def esc(valor):
    return html.escape(str(valor)) if valor is not None else ""


TEXTOS = {
    "pt": {
        "lang_label": "Idioma / Language",
        "pt_br": "Português (Brasil)",
        "en": "English",
        "enter_room": "Entrar na sala",
        "enter_room_subtitle": "Digite a senha combinada para acessar a dinâmica",
        "room_password": "Senha da sala",
        "room_placeholder": "Digite a senha do workshop",
        "enter_button": "Entrar",
        "password_required": "Digite uma senha para entrar.",
        "focus_default": "Defina o tema principal do workshop",
        "save_focus": "Salvar foco",
        "edit_focus": "Editar foco",
        "focus_required": "Digite um foco antes de salvar.",
        "tab_summary": "Resumo",
        "tab_focus": "Foco no Foco",
        "tab_barriers": "Principais Entraves",
        "tab_solutions": "Hipóteses de Solução",
        "tab_viability": "Viabilidade e Impacto",
    "summary_solution_label": "COMO RESOLVER?",
    "summary_solution_text": "Ainda em construção...",

    "summary_viability_label": "POR ONDE JÁ PODEMOS COMEÇAR?",
    "summary_viability_text": "Ainda em construção...",

        "focus_subtitle": "Onde queremos chegar",
        "barriers_subtitle": "O que nos impede?",
        "solutions_subtitle": "Como resolver?",
        "viability_subtitle": "Por onde já podemos começar?",
        "under_construction": "Ainda em construção...",
        "solutions_construction_help": "Essa etapa será utilizada para estruturar hipóteses de solução para os principais entraves identificados.",
        "viability_construction_help": "Essa etapa será utilizada para avaliar viabilidade, impacto e possíveis quick wins.",
        "summary_title": "Resumo",
        "summary_step_title": "Resumo do workshop",
        "summary_step_help": "Aqui aparecem os principais resultados consolidados das próximas abas.",
        "focus": "Foco",
        "meeting_focus": "FOCO DO WORKSHOP",
        "focus_not_defined": "O foco do workshop ainda não foi definido.",
        "focus_on_focus": "Foco no Foco",
        "focus_on_focus_caps": "FOCO NO FOCO",
        "focus_tie_summary": "Há empate no Foco no Foco. Faça a votação de desempate na aba Foco no Foco.",
        "focus_not_defined_vote": "O Foco no Foco ainda não foi definido pela votação.",
        "categorized_barriers": "Entraves categorizados",
        "current_room": "Sala atual",
        "team_step_title": "1. Nome da equipe",
        "team_step_help": "Digite o nome da equipe e o líder. Depois clique em salvar.",
        "time_step_minutes": "Tempo para essa etapa em minutos",
        "team_name": "Nome da equipe",
        "team_placeholder": "Exemplo: Time Céu Azul",
        "leader_name": "Líder da equipe",
        "leader_placeholder": "Exemplo: Ana",
        "save_team": "Salvar equipe",
        "edit_team": "Editar equipe",
        "team_label": "Equipe",
        "leader_label": "Líder",
        "postit_step_title": "2. Six Simplify",
        "postit_step_help": "Escreva uma frase com exatamente 6 palavras. Depois clique em adicionar.",
        "time_postits_minutes": "Tempo para escrever os post-its em minutos",
        "add_postit": "Adicionar post-it",
        "postit_placeholder": "Exemplo: Reduzir retrabalho entre áreas de engenharia",
        "words": "palavras",
        "missing_words": "Faltam palavras. O post-it precisa ter exatamente 6.",
        "too_many_words": "Tem palavras demais. O post-it precisa ter exatamente 6.",
        "save_team_before_postit": "Salve o nome da equipe antes de adicionar um post-it.",
        "exact_words": "O post-it precisa ter exatamente 6 palavras.",
        "postit_added": "Post-it adicionado!",
        "vote_step_title": "3. Vote nos post-its",
        "vote_step_help": "Leia os post-its e clique em votar. Se errar, clique em desfazer voto.",
        "votes": "Votos",
        "undo_vote": "Desfazer voto",
        "vote": "Votar",
        "no_postit": "Nenhum post-it disponível ainda nesta sala.",
        "result_step_title": "4. Veja o resultado",
        "result_step_help": "O post-it mais votado aparece abaixo. Se empatar, faça uma nova votação apenas com os empatados.",
        "tie_warning": "Houve empate. Faça uma nova votação apenas com os empatados.",
        "start_tie": "Iniciar votação de desempate",
        "result_will_appear": "O resultado aparecerá aqui após a votação.",
        "show_all": "Mostrar todos",
        "reset_votes": "Zerar votos",
        "barriers_title": "Principais Entraves",
        "add_barrier_title": "Adicionar entrave",
        "add_barrier_help": "Cada equipe pode adicionar quantos post-its quiser. Todos os participantes da mesma sala conseguirão visualizar e votar no mural completo.",
        "time_barriers_minutes": "Tempo para pensar nos entraves em minutos",
        "new_barrier": "Novo post-it de entrave",
        "barrier_placeholder": "Digite os entraves relacionados ao Foco no Foco (um entrave por vez)",
        "add_barrier_button": "Adicionar entrave",
        "save_team_before_barrier": "Salve o nome da equipe na aba Foco no Foco antes de adicionar entraves.",
        "barrier_required": "Digite o texto do entrave antes de adicionar.",
        "barrier_added": "Entrave adicionado!",
        "barriers_board": "Mural de entraves por equipe",
        "team_barriers_board": "Mural de entraves da equipe",
        "postits_count": "post-it(s)",
        "ranking_barriers": "Ranking dos entraves mais votados",
        "ranking_label": "RANKING DOS ENTRAVES",
        "top3": "Top 3 mais votados",
        "ranking_empty": "O ranking dos entraves aparecerá aqui após a votação.",
        "no_barriers": "Nenhum entrave adicionado ainda nesta sala.",
        "categorize_top3": "Categorizar entraves do Top 3",
        "category_name": "Nome da categoria",
        "category_placeholder": "Exemplo: Tecnologia",
        "choose_barriers": "Escolha os entraves",
        "save_category": "Salvar categoria",
        "category_required": "Digite o nome da categoria.",
        "choose_one_barrier": "Escolha pelo menos um entrave.",
        "category_created": "Categoria criada!",
        "category_after_top3": "A categorização aparecerá após existirem entraves no Top 3.",
        "created_categories": "Categorias criadas",
        "category_caps": "O QUE NOS IMPEDE?<br>CATEGORIA",
        "no_categories": "Nenhuma categoria criada ainda.",
        "first_place": "1º lugar",
        "second_place": "2º lugar",
        "third_place": "3º lugar",
        "timer_start": "Iniciar cronômetro",
        "timer_stop": "Parar cronômetro",
        "timer_finished": "Tempo encerrado!",
        "timer_shared_title": "Cronômetro da etapa",
        "timer_shared_help": "Defina o tempo e clique no relógio para iniciar ou parar para todos nesta sala.",
        "timer_minutes": "Tempo em minutos",
        "timer_click_start": "Clique no relógio para iniciar",
        "timer_running": "Cronômetro em andamento",
        "timer_stopped": "Cronômetro parado",
        "timer_remaining": "Faltam"
    },
    "en": {
        "lang_label": "Language / Idioma",
        "pt_br": "Português (Brasil)",
        "en": "English",
        "enter_room": "Enter room",
        "enter_room_subtitle": "Enter the agreed password to access the activity",
        "room_password": "Room password",
        "room_placeholder": "Enter the meeting password",
        "enter_button": "Enter",
        "password_required": "Enter a password to continue.",
        "focus_default": "Define the main topic of the meeting",
        "save_focus": "Save focus",
        "edit_focus": "Edit focus",
        "focus_required": "Enter a focus before saving.",
        "tab_summary": "Summary",
        "tab_focus": "Focus on Focus",
        "tab_barriers": "Main Barriers",
        "tab_solutions": "Solution Hypotheses",
        "tab_viability": "Feasibility and Impact",
    "summary_solution_label": "HOW CAN WE SOLVE IT?",
    "summary_solution_text": "Still under construction...",

    "summary_viability_label": "WHERE CAN WE START?",
    "summary_viability_text": "Still under construction...",

        "focus_subtitle": "Where we want to go",
        "barriers_subtitle": "What is stopping us?",
        "solutions_subtitle": "How can we solve it?",
        "viability_subtitle": "Where can we start already?",
        "under_construction": "Still under construction...",
        "solutions_construction_help": "This step will be used to structure solution hypotheses for the main barriers identified.",
        "viability_construction_help": "This step will be used to assess feasibility, impact, and possible quick wins.",
        "summary_title": "Summary",
        "summary_step_title": "Workshop summary",
        "summary_step_help": "This page consolidates the key outcomes from the following tabs.",
        "focus": "Focus",
        "meeting_focus": "MEETING FOCUS",
        "focus_not_defined": "The meeting focus has not been defined yet.",
        "focus_on_focus": "Focus on Focus",
        "focus_on_focus_caps": "FOCUS ON FOCUS",
        "focus_tie_summary": "There is a tie in Focus on Focus. Run the tie-break vote in the Focus on Focus tab.",
        "focus_not_defined_vote": "Focus on Focus has not been defined by voting yet.",
        "categorized_barriers": "Categorized barriers",
        "current_room": "Current room",
        "team_step_title": "1. Team name",
        "team_step_help": "Enter the team name and leader. Then click save.",
        "time_step_minutes": "Time for this step in minutes",
        "team_name": "Team name",
        "team_placeholder": "Example: BlueSky Team",
        "leader_name": "Team leader",
        "leader_placeholder": "Example: Ana",
        "save_team": "Save team",
        "edit_team": "Edit team",
        "team_label": "Team",
        "leader_label": "Leader",
        "postit_step_title": "2. Six Simplify",
        "postit_step_help": "Write a sentence with exactly 6 words. Then click add.",
        "time_postits_minutes": "Time to write post-its in minutes",
        "add_postit": "Add post-it",
        "postit_placeholder": "Example: Improve communication between critical internal areas",
        "words": "words",
        "missing_words": "You need more words. The post-it must have exactly 6.",
        "too_many_words": "Too many words. The post-it must have exactly 6.",
        "save_team_before_postit": "Save the team name before adding a post-it.",
        "exact_words": "The post-it must have exactly 6 words.",
        "postit_added": "Post-it added!",
        "vote_step_title": "3. Vote on post-its",
        "vote_step_help": "Read the post-its and click vote. If you make a mistake, click undo vote.",
        "votes": "Votes",
        "undo_vote": "Undo vote",
        "vote": "Vote",
        "no_postit": "No post-its available in this room yet.",
        "result_step_title": "4. See the result",
        "result_step_help": "The most voted post-it appears below. If there is a tie, run a new vote only with tied post-its.",
        "tie_warning": "There is a tie. Run a new vote only with the tied post-its.",
        "start_tie": "Start tie-break vote",
        "result_will_appear": "The result will appear here after voting.",
        "show_all": "Show all",
        "reset_votes": "Reset votes",
        "barriers_title": "Main Barriers",
        "add_barrier_title": "Add barrier",
        "add_barrier_help": "Each team can add as many post-its as needed. Everyone in the same room can view and vote on the full board.",
        "time_barriers_minutes": "Time to think about barriers in minutes",
        "new_barrier": "New barrier post-it",
        "barrier_placeholder": "Enter the main barrier identified by the team",
        "add_barrier_button": "Add barrier",
        "save_team_before_barrier": "Save the team name in the Focus on Focus tab before adding barriers.",
        "barrier_required": "Enter the barrier text before adding.",
        "barrier_added": "Barrier added!",
        "barriers_board": "Barrier board by team",
        "team_barriers_board": "Team barrier board",
        "postits_count": "post-it(s)",
        "ranking_barriers": "Ranking of most voted barriers",
        "ranking_label": "BARRIER RANKING",
        "top3": "Top 3 most voted",
        "ranking_empty": "The barrier ranking will appear here after voting.",
        "no_barriers": "No barriers added in this room yet.",
        "categorize_top3": "Categorize Top 3 barriers",
        "category_name": "Category name",
        "category_placeholder": "Example: Technology",
        "choose_barriers": "Choose barriers",
        "save_category": "Save category",
        "category_required": "Enter the category name.",
        "choose_one_barrier": "Choose at least one barrier.",
        "category_created": "Category created!",
        "category_after_top3": "Categorization will appear after there are barriers in the Top 3.",
        "created_categories": "Created categories",
        "category_caps": "WHAT IS STOPPING US?<br>CATEGORY",
        "no_categories": "No categories created yet.",
        "first_place": "1st place",
        "second_place": "2nd place",
        "third_place": "3rd place",
        "timer_start": "Start timer",
        "timer_stop": "Stop timer",
        "timer_finished": "Time is up!",
        "timer_shared_title": "Step timer",
        "timer_shared_help": "Set the time and click the clock to start or stop it for everyone in this room.",
        "timer_minutes": "Time in minutes",
        "timer_click_start": "Click the clock to start",
        "timer_running": "Timer running",
        "timer_stopped": "Timer stopped",
        "timer_remaining": "Remaining"
    }
}


def t(chave):
    idioma = st.session_state.get("idioma", "pt")
    return TEXTOS.get(idioma, TEXTOS["pt"]).get(chave, TEXTOS["pt"].get(chave, chave))


def contar_palavras(texto):
    return len(texto.strip().split())


def mostrar_cronometro_compartilhado(sala_atual, aba_timer, valor_padrao=5):

    cursor.execute("""
    SELECT inicio, duracao, ativo
    FROM timers
    WHERE sala = ? AND aba = ?
    """, (sala_atual, aba_timer))

    timer_banco = cursor.fetchone()

    inicio = None
    duracao = int(valor_padrao * 60)
    ativo = 0

    if timer_banco:
        inicio, duracao, ativo = timer_banco

    st.markdown(
        f"""
<div class="timer-card">
<div class="timer-title">{t("timer_shared_title")}</div>
<div class="timer-help">{t("timer_shared_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    tempo_restante = None
    minutos = max(int(duracao // 60), 1)
    segundos = 0

    if ativo and inicio:

        st_autorefresh(
            interval=1000,
            key=f"refresh_timer_{aba_timer}"
        )

        tempo_passado = int(time.time() - inicio)
        tempo_restante = max(int(duracao) - tempo_passado, 0)

        minutos = tempo_restante // 60
        segundos = tempo_restante % 60

    if st.session_state.get("is_mobile", False):

        minutos_configurados = st.number_input(
            t("timer_minutes"),
            min_value=1,
            max_value=120,
            value=max(int(duracao // 60), 1),
            key=f"tempo_{aba_timer}"
        )

        st.markdown('<div class="timer-mobile-row">', unsafe_allow_html=True)

        col_info_mobile, col_relogio_mobile = st.columns([1.55, 1])

        with col_info_mobile:

            if ativo and inicio:

                st.markdown(
                    f"""
<div class="timer-mobile-info">
    <div class="timer-mobile-label">{t("timer_running")}</div>
    <div class="timer-mobile-time">{minutos:02d}:{segundos:02d}</div>
</div>
""",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
<div class="timer-mobile-info">
    <div class="timer-mobile-label">{t("timer_click_start")}</div>
    <div class="timer-mobile-time">{int(minutos_configurados):02d}:00</div>
</div>
""",
                    unsafe_allow_html=True
                )

        with col_relogio_mobile:

            with st.container(key=f"timer_area_{aba_timer}"):

                botao_relogio = "⏹️" if ativo else "⏱️"

                if st.button(
                    botao_relogio,
                    key=f"botao_timer_{aba_timer}"
                ):

                    if ativo:
                        cursor.execute("""
                        INSERT INTO timers (sala, aba, inicio, duracao, ativo)
                        VALUES (?, ?, NULL, ?, 0)
                        ON CONFLICT(sala, aba)
                        DO UPDATE SET
                            inicio = NULL,
                            duracao = excluded.duracao,
                            ativo = 0
                        """, (
                            sala_atual,
                            aba_timer,
                            int(minutos_configurados * 60)
                        ))

                        conn.commit()
                        st.rerun()

                    else:
                        cursor.execute("""
                        INSERT INTO timers (sala, aba, inicio, duracao, ativo)
                        VALUES (?, ?, ?, ?, 1)
                        ON CONFLICT(sala, aba)
                        DO UPDATE SET
                            inicio = excluded.inicio,
                            duracao = excluded.duracao,
                            ativo = 1
                        """, (
                            sala_atual,
                            aba_timer,
                            time.time(),
                            int(minutos_configurados * 60)
                        ))

                        conn.commit()
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        col_tempo, col_display, col_relogio, col_espaco = st.columns([1.05, 0.58, 0.32, 1.55])

        with col_tempo:

            minutos_configurados = st.number_input(
                t("timer_minutes"),
                min_value=1,
                max_value=120,
                value=max(int(duracao // 60), 1),
                key=f"tempo_{aba_timer}"
            )

        with col_display:

            if ativo and inicio:

                st.markdown(
                    f"""
<div class="timer-desktop-display">
<div class="timer-display">{minutos:02d}:{segundos:02d}</div>
<div class="timer-status">{t("timer_running")}</div>
</div>
""",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
<div class="timer-desktop-display">
<div class="timer-display">{int(minutos_configurados):02d}:00</div>
<div class="timer-status">{t("timer_click_start")}</div>
</div>
""",
                    unsafe_allow_html=True
                )

        with col_relogio:

            st.markdown('<div class="timer-desktop-button">', unsafe_allow_html=True)

            with st.container(key=f"timer_area_{aba_timer}"):

                botao_relogio = "⏹️" if ativo else "⏱️"

                if st.button(
                    botao_relogio,
                    key=f"botao_timer_{aba_timer}"
                ):

                    if ativo:
                        cursor.execute("""
                        INSERT INTO timers (sala, aba, inicio, duracao, ativo)
                        VALUES (?, ?, NULL, ?, 0)
                        ON CONFLICT(sala, aba)
                        DO UPDATE SET
                            inicio = NULL,
                            duracao = excluded.duracao,
                            ativo = 0
                        """, (
                            sala_atual,
                            aba_timer,
                            int(minutos_configurados * 60)
                        ))

                        conn.commit()
                        st.rerun()

                    else:
                        cursor.execute("""
                        INSERT INTO timers (sala, aba, inicio, duracao, ativo)
                        VALUES (?, ?, ?, ?, 1)
                        ON CONFLICT(sala, aba)
                        DO UPDATE SET
                            inicio = excluded.inicio,
                            duracao = excluded.duracao,
                            ativo = 1
                        """, (
                            sala_atual,
                            aba_timer,
                            time.time(),
                            int(minutos_configurados * 60)
                        ))

                        conn.commit()
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    if ativo and inicio:

        st.progress(
            tempo_restante / int(duracao)
            if int(duracao) > 0
            else 0
        )

        if tempo_restante == 0:

            cursor.execute("""
            UPDATE timers
            SET ativo = 0
            WHERE sala = ? AND aba = ?
            """, (
                sala_atual,
                aba_timer
            ))

            conn.commit()
            st.error(t("timer_finished"))
            st.rerun()


def mostrar_pilula_timer_fixa(sala_atual, aba_timer):

    cursor.execute("""
    SELECT inicio, duracao, ativo
    FROM timers
    WHERE sala = ? AND aba = ?
    """, (sala_atual, aba_timer))

    timer_banco = cursor.fetchone()

    if not timer_banco:
        return

    inicio, duracao, ativo = timer_banco

    if not ativo or not inicio:
        return

    tempo_passado = int(time.time() - inicio)
    tempo_restante = max(int(duracao) - tempo_passado, 0)

    minutos = tempo_restante // 60
    segundos = tempo_restante % 60

    st.markdown(
        f"""
<div class="timer-fixed-pill-global">
    <div>
        <div class="timer-fixed-pill-label">{t("timer_remaining")}</div>
        <div class="timer-fixed-pill-time">{minutos:02d}:{segundos:02d}</div>
    </div>
    <div class="timer-fixed-pill-icon">⏱️</div>
</div>
""",
        unsafe_allow_html=True
    )


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


def buscar_rankings_entraves(sala_atual):

    cursor.execute("""
    SELECT equipe, texto, votos, id
    FROM entraves
    WHERE sala = ?
    AND votos > 0
    ORDER BY votos DESC, id ASC
    """, (sala_atual,))

    entraves_mais_votados = cursor.fetchall()

    rankings = []
    votos_ja_usados = []

    for item in entraves_mais_votados:
        votos_item = item[2]

        if votos_item not in votos_ja_usados:
            votos_ja_usados.append(votos_item)

        posicao = votos_ja_usados.index(votos_item) + 1

        if posicao <= 3:
            rankings.append((posicao, item))

    return rankings


def mostrar_categorias(sala_atual, permitir_remover=False):

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

    if not categorias_salvas:
        st.info(t("no_categories"))
        return

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
<div class="resultado-label">{t("category_caps")}</div>
<div class="resultado-texto">{esc(categoria)}</div>
</div>
""",
            unsafe_allow_html=True
        )

        colunas_categoria = (
            [st.container()]
            if st.session_state.get("is_mobile", False)
            else st.columns(3, gap="large")
        )

        for i, item_categoria in enumerate(itens_categoria):

            categoria_id = item_categoria[0]
            equipe_cat = item_categoria[1]
            texto_cat = item_categoria[2]
            votos_cat = item_categoria[3]

            with colunas_categoria[i % len(colunas_categoria)]:

                st.markdown(
                    f"""
<div class="desktop-card-html" style="
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
{t("team_label")}: {esc(equipe_cat)} • {votos_cat} {t("votes").lower()}
</div>
<div class="texto-card" style="
    color:#111827;
    font-size:22px;
    line-height:1.45;
    font-weight:800;
">
{esc(texto_cat)}
</div>
</div>
""",
                    unsafe_allow_html=True
                )

                if permitir_remover:

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


# =========================
# SESSION STATE
# =========================

if "sala" not in st.session_state:
    st.session_state.sala = None

if "idioma" not in st.session_state:
    st.session_state.idioma = "pt"

if "postits_votados" not in st.session_state:
    st.session_state.postits_votados = set()

if "entraves_votados" not in st.session_state:
    st.session_state.entraves_votados = set()

if "foco_salvo" not in st.session_state:
    st.session_state.foco_salvo = ""

if "editando_foco" not in st.session_state:
    st.session_state.editando_foco = True


if "esconder_cabecalho_fixo" not in st.session_state:
    st.session_state.esconder_cabecalho_fixo = False


# =========================
# ENTRADA POR SENHA / SALA
# =========================

if st.session_state.sala is None:

    st.markdown(
        """
<div class="landing-title">
<div class="landing-embraer">EMBRAER</div>
<div class="landing-main">SIX SIMPLIFY</div>
<div class="landing-sub">Workshop</div>
</div>
""",
        unsafe_allow_html=True
    )

    idioma_opcao = st.selectbox(
        t("lang_label"),
        [t("pt_br"), t("en")],
        index=0 if st.session_state.idioma == "pt" else 1,
        key="seletor_idioma"
    )

    st.session_state.idioma = "en" if idioma_opcao == t("en") else "pt"

    st.markdown(
        f"""
<div class="header-foco">
<div class="header-title">{t("enter_room")}</div>
<div class="header-subtitle">{t("enter_room_subtitle")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    senha_sala = st.text_input(
        t("room_password"),
        type="password",
        placeholder=t("room_placeholder")
    )

    equipe_url = st.query_params.get("equipe", "")
    lider_url = st.query_params.get("lider", "")

    equipe_login = ""
    lider_login = ""

    if equipe_url:

        st.markdown(
            """
<div class="step-card">
<div class="step-title">Equipe já identificada</div>
<div class="step-help">Confirme ou edite sua equipe antes de entrar novamente.</div>
</div>
""",
            unsafe_allow_html=True
        )

        equipe_login = st.text_input(
            t("team_name"),
            value=equipe_url,
            placeholder=t("team_placeholder"),
            key="equipe_login"
        )

        lider_login = st.text_input(
            t("leader_name"),
            value=lider_url,
            placeholder=t("leader_placeholder"),
            key="lider_login"
        )

    if st.button(t("enter_button")):
        if senha_sala.strip():
            st.session_state.sala = senha_sala.strip()
            st.session_state.postits_votados = set()
            st.session_state.entraves_votados = set()

            if equipe_url:
                st.session_state.nome_equipe_salvo = equipe_login.strip()
                st.session_state.lider_equipe_salvo = lider_login.strip()
                st.session_state.editando_equipe = False

                if equipe_login.strip():
                    st.query_params["equipe"] = equipe_login.strip()

                if lider_login.strip():
                    st.query_params["lider"] = lider_login.strip()

            st.rerun()
        else:
            st.warning(t("password_required"))

    st.stop()

sala_atual = st.session_state.sala

if st.query_params.get("equipe", "") and not st.session_state.get("nome_equipe_salvo", ""):
    st.session_state.nome_equipe_salvo = st.query_params.get("equipe", "")
    st.session_state.editando_equipe = False

if st.query_params.get("lider", "") and not st.session_state.get("lider_equipe_salvo", ""):
    st.session_state.lider_equipe_salvo = st.query_params.get("lider", "")

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
# NAVEGAÇÃO
# =========================

aba_atual = st.radio(
    "Navegação",
    [
        t("tab_summary"),
        t("tab_focus"),
        t("tab_barriers"),
        t("tab_solutions"),
        t("tab_viability")
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="aba_atual"
)



# CSS condicional para esconder/mostrar abas junto com o cabeçalho
if st.session_state.get("esconder_cabecalho_fixo", False):

    st.markdown(
        """
<style>
div[role="radiogroup"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}
</style>
""",
        unsafe_allow_html=True
    )



# CSS CONDICIONAL PROVA DE STREAMLIT — ESCONDE CABEÇALHO E ABAS
if st.session_state.get("esconder_cabecalho_fixo", False):

    st.markdown(
        """
<style>
@media (max-width: 768px) {
    div[role="radiogroup"],
    .fixed-workshop-header,
    .fixed-workshop-header-spacer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        width: 0 !important;
        max-width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
        position: absolute !important;
        top: -9999px !important;
        left: -9999px !important;
    }

    .summary-header-mobile-spacer,
    .summary-mobile-spacer {
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
}
</style>
""",
        unsafe_allow_html=True
    )


# Pílula fixa do cronômetro da aba atual
if aba_atual == t("tab_focus"):
    mostrar_pilula_timer_fixa(
        sala_atual,
        "foco_no_foco"
    )

if aba_atual == t("tab_barriers"):
    mostrar_pilula_timer_fixa(
        sala_atual,
        "principais_entraves"
    )


# Botão flutuante para esconder/mostrar cabeçalho fixo
if aba_atual != t("tab_summary"):

    texto_toggle_cabecalho = (
        "Mostrar cabeçalho"
        if st.session_state.esconder_cabecalho_fixo
        else "Esconder cabeçalho"
    )

    with st.container(key="toggle_cabecalho_fixo"):

        if st.button(texto_toggle_cabecalho):
            st.session_state.esconder_cabecalho_fixo = (
                not st.session_state.esconder_cabecalho_fixo
            )
            st.rerun()



# Correção real: esconder cabeçalho e abas sem deixar sobra no mobile
if st.session_state.get("esconder_cabecalho_fixo", False):

    st.markdown(
        """
<style>
@media (max-width: 768px) {
    div[role="radiogroup"],
    .fixed-workshop-header,
    .fixed-workshop-header-spacer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        top: -9999px !important;
        left: -9999px !important;
    }
}
</style>
""",
        unsafe_allow_html=True
    )


# =========================
# HEADER DINÂMICO
# =========================

vencedores_header, _, empate_header = buscar_mais_votados(
    sala_atual
)

foco_no_foco_header = ""

if vencedores_header and not empate_header:
    foco_no_foco_header = vencedores_header[0][2]

if aba_atual == t("tab_barriers") and foco_no_foco_header:

    titulo_header = t("focus_on_focus")
    subtitulo_header = foco_no_foco_header

else:

    titulo_header = t("focus")

    subtitulo_header = (
        st.session_state.foco_salvo
        if st.session_state.foco_salvo
        else t("focus_default")
    )

if aba_atual == t("tab_summary"):

    if st.session_state.get("is_mobile", False):

        st.markdown(
            """
<div class="summary-header-mobile-spacer"></div>
""",
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
<div class="header-foco">
    <div class="header-title">{esc(titulo_header)}</div>
    <div class="header-subtitle">{esc(subtitulo_header)}</div>
</div>
""",
        unsafe_allow_html=True
    )

else:

    if not st.session_state.esconder_cabecalho_fixo:

        st.markdown(
            f"""
<div class="fixed-workshop-header">
    <div class="header-foco">
        <div class="header-title">{esc(titulo_header)}</div>
        <div class="header-subtitle">{esc(subtitulo_header)}</div>
    </div>
</div>
<div class="fixed-workshop-header-spacer"></div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
<style>
/* Esconde também as abas fixas quando o cabeçalho está oculto */
div[role="radiogroup"]{
    display:none !important;
}
</style>

<div style="height: 20px;"></div>
""",
            unsafe_allow_html=True
        )

if aba_atual == t("tab_summary"):

    if st.session_state.editando_foco:

        foco_digitado = st.text_input(
            label="campo_foco",
            value=st.session_state.foco_salvo,
            placeholder=t("focus_default"),
            key="campo_foco",
            label_visibility="collapsed"
        )

        if st.button(t("save_focus")):

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
                st.warning(t("focus_required"))

    else:

        if st.button(t("edit_focus")):
            st.session_state.editando_foco = True
            st.rerun()


# =========================
# ABA 0 - SUMMARY
# =========================

if aba_atual == t("tab_summary"):

    if st.session_state.get("is_mobile", False):

        st.markdown(
            """
<div class="summary-mobile-spacer"></div>
""",
            unsafe_allow_html=True
        )

    st.title(t("summary_title"))

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("summary_step_title")}</div>\n<div class="step-help">{t("summary_step_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(f"## {t('focus')}")

    if st.session_state.foco_salvo:

        st.markdown(
            f"""
<div class="resultado-final-header">
<div class="resultado-label">{t("meeting_focus")}</div>
<div class="resultado-texto">{esc(st.session_state.foco_salvo)}</div>
</div>
""",
            unsafe_allow_html=True
        )

    else:
        st.info(t("focus_not_defined"))

    st.markdown(f"## {t('focus_on_focus')}")

    vencedores_summary, _, tem_empate_summary = buscar_mais_votados(
        sala_atual
    )

    if vencedores_summary and not tem_empate_summary:

        st.markdown(
            f"""
<div class="resultado-final-header">
<div class="resultado-label">{t("focus_on_focus_caps")}</div>
<div class="resultado-texto">{esc(vencedores_summary[0][2])}</div>
</div>
""",
            unsafe_allow_html=True
        )

    elif tem_empate_summary:

        st.warning(t("focus_tie_summary"))

    else:

        st.info(t("focus_not_defined_vote"))

    st.markdown(f"## {t('categorized_barriers')}")

    mostrar_categorias(
        sala_atual,
        permitir_remover=False
    )



    # =========================
    # HIPÓTESES DE SOLUÇÃO
    # =========================

    st.markdown("## Hipóteses de Solução")

    st.markdown(
        """
<div class="resultado-final-header">
<div class="resultado-label">COMO RESOLVER?</div>
<div class="resultado-texto">
Ainda em construção...
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # =========================
    # VIABILIDADE E IMPACTO
    # =========================

    st.markdown("## Viabilidade e Impacto")

    st.markdown(
        """
<div class="resultado-final-header">
<div class="resultado-label">POR ONDE JÁ PODEMOS COMEÇAR?</div>
<div class="resultado-texto">
Ainda em construção...
</div>
</div>
""",
        unsafe_allow_html=True
    )


# =========================
# ABA 1 - FOCO NO FOCO
# =========================

if aba_atual == t("tab_focus"):

    st.title(t("focus_on_focus"))

    st.markdown(
        f"""
<div style="
    font-size:24px;
    font-weight:500;
    color:#222;
    margin-top:-22px;
    margin-bottom:4px;
    opacity:0.92;
">
{t("focus_subtitle")}
</div>
""",
        unsafe_allow_html=True
    )

    st.caption(f"{t('current_room')}: {sala_atual}")

    mostrar_cronometro_compartilhado(
        sala_atual,
        "foco_no_foco",
        valor_padrao=5
    )

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("team_step_title")}</div>\n<div class="step-help">{t("team_step_help")}</div>
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

    if st.session_state.editando_equipe:

        nome_equipe_digitado = st.text_input(
            t("team_name"),
            value=st.session_state.nome_equipe_salvo,
            placeholder=t("team_placeholder")
        )

        lider_equipe_digitado = st.text_input(
            t("leader_name"),
            value=st.session_state.lider_equipe_salvo,
            placeholder=t("leader_placeholder")
        )

        if st.button(t("save_team")):

            st.session_state.nome_equipe_salvo = nome_equipe_digitado.strip()
            st.session_state.lider_equipe_salvo = lider_equipe_digitado.strip()
            st.session_state.editando_equipe = False

            if nome_equipe_digitado.strip():
                st.query_params["equipe"] = nome_equipe_digitado.strip()

            if lider_equipe_digitado.strip():
                st.query_params["lider"] = lider_equipe_digitado.strip()

            st.rerun()

    else:

        st.markdown(
            f"""
<div class="bloco-azul info-equipe">
<strong>{t("team_label")}:</strong> {esc(st.session_state.nome_equipe_salvo)}<br>\n<strong>{t("leader_label")}:</strong> {esc(st.session_state.lider_equipe_salvo)}
</div>
""",
            unsafe_allow_html=True
        )

        if st.button(t("edit_team")):
            st.session_state.editando_equipe = True
            st.rerun()

    nome_equipe = st.session_state.nome_equipe_salvo

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("postit_step_title")}</div>\n<div class="step-help">{t("postit_step_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    novo_postit = st.text_area(
        t("add_postit"),
        placeholder=t("postit_placeholder")
    )

    qtd_palavras = contar_palavras(novo_postit)

    st.caption(f"{qtd_palavras}/6 {t('words')}")

    if qtd_palavras < 6 and qtd_palavras > 0:
        st.warning(t("missing_words"))

    if qtd_palavras > 6:
        st.error(t("too_many_words"))

    if st.button(t("add_postit")):

        if not nome_equipe.strip():
            st.warning(t("save_team_before_postit"))
        elif qtd_palavras != 6:
            st.error(t("exact_words"))
        else:
            cursor.execute("""
            INSERT INTO postits (equipe, texto, votos, ativo, sala)
            VALUES (?, ?, 0, 1, ?)
            """, (nome_equipe, novo_postit, sala_atual))

            conn.commit()
            st.success(t("postit_added"))
            st.rerun()

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("vote_step_title")}</div>\n<div class="step-help">{t("vote_step_help")}</div>
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

        if st.session_state.get("is_mobile", False):

            # Mobile: mantém 1 post-it por vez
            for postit_id, equipe, texto, votos in postits:

                classe_postit = (
                    "postit-votado"
                    if postit_id in st.session_state.postits_votados
                    else "postit"
                )

                st.markdown(
                    f"""
<div class="{classe_postit}">
<h4>{esc(equipe)}</h4>
<div class="postit-texto">{esc(texto)}</div>
<div class="votos">{t("votes")}: {votos}</div>
</div>
""",
                    unsafe_allow_html=True
                )

                if postit_id in st.session_state.postits_votados:

                    if st.button(
                        t("undo_vote"),
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
                        t("vote"),
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

            # Desktop: post-it + botão ficam dentro da mesma coluna
            colunas_postits = st.columns(3, gap="large")

            for i, (postit_id, equipe, texto, votos) in enumerate(postits):

                with colunas_postits[i % len(colunas_postits)]:

                    classe_postit = (
                        "postit-votado"
                        if postit_id in st.session_state.postits_votados
                        else "postit"
                    )

                    st.markdown(
                        f"""
<div class="desktop-card-html {classe_postit}" style="
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    min-height:260px;
">
<div>
<h4>{esc(equipe)}</h4>
<div class="postit-texto texto-card">{esc(texto)}</div>
</div>
<div class="votos">{t("votes")}: {votos}</div>
</div>
""",
                        unsafe_allow_html=True
                    )

                    if postit_id in st.session_state.postits_votados:

                        if st.button(
                            t("undo_vote"),
                            key=f"desfazer_{postit_id}",
                            use_container_width=True
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
                            t("vote"),
                            key=f"votar_{postit_id}",
                            use_container_width=True
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
        st.info(t("no_postit"))

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("result_step_title")}</div>\n<div class="step-help">{t("result_step_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(f"## {t('focus_on_focus')}")

    vencedores, _, tem_empate = buscar_mais_votados(sala_atual)

    if vencedores and not tem_empate:

        st.markdown(
            f"""
<div class="resultado-final-header">
<div class="resultado-label">{t("focus_on_focus_caps")}</div>
<div class="resultado-texto">{esc(vencedores[0][2])}</div>
</div>
""",
            unsafe_allow_html=True
        )

    elif tem_empate:

        st.warning(t("tie_warning"))

        if st.button(t("start_tie")):

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
        st.info(t("result_will_appear"))

    if st.button(t("show_all")):
        cursor.execute(
            "UPDATE postits SET ativo = 1 WHERE sala = ?",
            (sala_atual,)
        )
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()

    if st.button(t("reset_votes")):
        cursor.execute(
            "UPDATE postits SET votos = 0 WHERE sala = ?",
            (sala_atual,)
        )
        conn.commit()
        st.session_state.postits_votados = set()
        st.rerun()


# =========================
# ABA 2 - PRINCIPAIS ENTRAVES
# =========================

if aba_atual == t("tab_barriers"):

    st.title(t("barriers_title"))

    st.markdown(
        f"""
<div style="
    font-size:24px;
    font-weight:500;
    color:#222;
    margin-top:-18px;
    margin-bottom:10px;
    opacity:0.92;
">
{t("barriers_subtitle")}
</div>
""",
        unsafe_allow_html=True
    )

    mostrar_cronometro_compartilhado(
        sala_atual,
        "principais_entraves",
        valor_padrao=7
    )

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("add_barrier_title")}</div>\n<div class="step-help">{t("add_barrier_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )

    equipe_entrave = st.session_state.nome_equipe_salvo

    if "limpar_campo_entrave" not in st.session_state:
        st.session_state["limpar_campo_entrave"] = False

    if st.session_state["limpar_campo_entrave"]:
        st.session_state["campo_entrave"] = ""
        st.session_state["limpar_campo_entrave"] = False

    novo_entrave = st.text_area(
        t("new_barrier"),
        placeholder=t("barrier_placeholder"),
        key="campo_entrave"
    )

    if st.button(t("add_barrier_button"), key="botao_adicionar_entrave"):

        if not equipe_entrave.strip():
            st.warning(t("save_team_before_barrier"))

        elif not novo_entrave.strip():
            st.warning(t("barrier_required"))

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
            st.session_state["limpar_campo_entrave"] = True
            st.success(t("barrier_added"))
            st.rerun()

    st.markdown(f"## {t('barriers_board')}")

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
{esc(equipe)}
</div>
<div style="
    color:#55708f;
    font-size:17px;
    font-weight:600;
    margin-top:6px;
">
{t("team_barriers_board")}
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
{len(lista_entraves)} {t("postits_count")}
</div>
</div>
</div>
""",
                unsafe_allow_html=True
            )

            # Desktop: 3 colunas lado a lado | Mobile: 1 coluna
            if st.session_state.get("is_mobile", False):
                colunas_mural = st.columns(1)
            else:
                colunas_mural = st.columns(3, gap="large")

            for i, (entrave_id, texto, votos) in enumerate(lista_entraves):

                with colunas_mural[i % len(colunas_mural)]:

                    foi_votado = entrave_id in st.session_state.entraves_votados

                    cor_postit = "#fbcfe8" if foi_votado else cor_time
                    borda = "3px solid #ec4899" if foi_votado else "2px solid rgba(0,47,95,0.18)"

                    html_postit = f"""
<div class="desktop-card-html" style="
    background:{cor_postit};
    padding:24px;
    border-radius:22px;
    min-height:240px;
    margin-bottom:14px;
    color:#111827;
    border:{borda};
    box-shadow:0 6px 16px rgba(15,23,42,0.08);
">
<div class="texto-card" style="
    color:#111827;
    font-size:23px;
    line-height:1.45;
    font-weight:800;
">
{esc(texto)}
</div>
<div style="
    margin-top:16px;
    color:#002f5f;
    font-size:18px;
    font-weight:800;
">
{t("votes")}: {votos}
</div>
</div>
"""

                    st.markdown(html_postit, unsafe_allow_html=True)

                    if foi_votado:

                        if st.button(
                            t("undo_vote"),
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
                            t("vote"),
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

        st.markdown(f"## {t('ranking_barriers')}")

        rankings = buscar_rankings_entraves(
            sala_atual
        )

        if rankings:

            st.markdown(
                f"""
<div class="resultado-final-header">
<div class="resultado-label">{t("ranking_label")}</div>\n<div class="resultado-texto">{t("top3")}</div>
</div>
""",
                unsafe_allow_html=True
            )

            colunas_ranking = (
                [st.container()]
                if st.session_state.get("is_mobile", False)
                else st.columns(3, gap="large")
            )

            for i, (posicao, (equipe_top, texto_top, votos_top, _)) in enumerate(rankings):

                with colunas_ranking[i % len(colunas_ranking)]:

                    if posicao == 1:
                        titulo_ranking = t("first_place")
                        cor_ranking = "#e79eff"
                        borda_ranking = "#8f7193"
                    elif posicao == 2:
                        titulo_ranking = t("second_place")
                        cor_ranking = "#dbeafe"
                        borda_ranking = "#2563eb"
                    else:
                        titulo_ranking = t("third_place")
                        cor_ranking = "#c7f7f7"
                        borda_ranking = "#96c4c4"

                    st.markdown(
                        f"""
<div class="desktop-card-html" style="
    background:{cor_ranking};
    padding:26px;
    border-radius:22px;
    min-height:240px;
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
{t("team_label")}: {esc(equipe_top)}
</div>
<div class="texto-card" style="
    color:#111827;
    font-size:24px;
    line-height:1.45;
    font-weight:850;
">
{esc(texto_top)}
</div>
</div>
""",
                        unsafe_allow_html=True
                    )

        else:
            st.info(t("ranking_empty"))

    else:
        st.info(t("no_barriers"))

    st.markdown(f"## {t('categorize_top3')}")

    if "limpar_categoria" not in st.session_state:
        st.session_state["limpar_categoria"] = False

    if st.session_state["limpar_categoria"]:
        st.session_state["nova_categoria_entraves"] = ""
        st.session_state["entraves_para_categoria"] = []
        st.session_state["limpar_categoria"] = False

    rankings = buscar_rankings_entraves(
        sala_atual
    )

    if rankings:

        opcoes_top3 = {
            f"{posicao}º lugar | {item[0]} | {item[1]}": item
            for posicao, item in rankings
        }

        nova_categoria = st.text_input(
            t("category_name"),
            placeholder=t("category_placeholder"),
            key="nova_categoria_entraves"
        )

        entraves_escolhidos = st.multiselect(
            t("choose_barriers"),
            options=list(opcoes_top3.keys()),
            key="entraves_para_categoria",
            placeholder=t("choose_barriers")
        )

        if st.button(t("save_category")):

            if not nova_categoria.strip():
                st.warning(t("category_required"))

            elif not entraves_escolhidos:
                st.warning(t("choose_one_barrier"))

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

                st.success(t("category_created"))
                st.rerun()

    else:
        st.info(t("category_after_top3"))

    st.markdown(f"## {t('created_categories')}")

    mostrar_categorias(
        sala_atual,
        permitir_remover=True
    )

st.markdown("""
<style>
@media (min-width: 769px) {

    .fixed-workshop-header .header-foco {
        padding: 18px 24px !important;
        border-radius: 22px !important;
    }

    .fixed-workshop-header .header-title {
        font-size: 42px !important;
        line-height: 1 !important;
        margin-bottom: 6px !important;
    }

    .fixed-workshop-header .header-subtitle {
        font-size: 22px !important;
        line-height: 1.2 !important;
    }

    div[data-testid="column"] {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
<style>
@media (min-width: 769px) {

    .desktop-card-html {
        min-height: 260px !important;
        height: 260px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    .desktop-card-html .texto-card {
        max-height: 145px !important;
        overflow: hidden !important;
    }

    .fixed-workshop-header .header-foco {
        padding: 18px 24px !important;
        border-radius: 22px !important;
    }

    .fixed-workshop-header .header-title {
        font-size: 42px !important;
        line-height: 1 !important;
        margin-bottom: 6px !important;
    }

    .fixed-workshop-header .header-subtitle {
        font-size: 22px !important;
        line-height: 1.2 !important;
    }

    .fixed-workshop-header-spacer {
        height: 300px !important;
    }

    div[data-testid="column"] {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
@media (min-width: 769px) {

    .timer-desktop-layout {
        display: grid !important;
        grid-template-columns: 0.85fr 0.55fr 0.35fr 1fr !important;
        align-items: end !important;
        gap: 10px !important;
        margin-top: 10px !important;
        margin-bottom: 24px !important;
    }

    .timer-desktop-layout [data-testid="stNumberInput"] {
        max-width: 280px !important;
    }

    .timer-desktop-layout [data-testid="stNumberInput"] > div {
        max-width: 280px !important;
    }

    .timer-desktop-display {
        text-align: center !important;
        padding-bottom: 4px !important;
    }

    .timer-desktop-display .timer-display {
        font-size: 52px !important;
        margin-top: 0 !important;
    }

    .timer-desktop-display .timer-status {
        font-size: 17px !important;
        margin-top: 8px !important;
    }

    .timer-desktop-button {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding-bottom: 0 !important;
    }

    .timer-desktop-button .stButton > button {
        min-height: 118px !important;
        height: 118px !important;
        width: 118px !important;
        border-radius: 999px !important;
        font-size: 54px !important;
        padding: 0 !important;
        box-shadow: 0 14px 32px rgba(0,47,95,0.26) !important;
    }

    .timer-desktop-button .stButton > button p {
        font-size: 54px !important;
        line-height: 1 !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
@media (min-width: 769px) {
    .timer-desktop-display {
        text-align: left !important;
        padding-top: 12px !important;
    }

    .timer-desktop-display .timer-display {
        text-align: left !important;
        font-size: 52px !important;
    }

    .timer-desktop-display .timer-status {
        text-align: left !important;
        font-size: 17px !important;
        white-space: nowrap !important;
    }

    .timer-desktop-button {
        justify-content: flex-start !important;
        padding-top: 0 !important;
    }

    .timer-desktop-button .stButton > button {
        margin-left: 0 !important;
        margin-right: auto !important;
    }

    .st-key-tempo_foco_no_foco,
    .st-key-tempo_principais_entraves,
    div[data-testid="stNumberInput"] {
        max-width: 320px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
@media (min-width: 769px) {
    .timer-fixed-pill-global {
        top: 195px !important;
        right: 22px !important;
        bottom: auto !important;
        transform: none !important;
        z-index: 2147483600 !important;
    }

    .fixed-workshop-header {
        width: min(760px, calc(100vw - 360px)) !important;
        left: calc(50% - 105px) !important;
        transform: translateX(-50%) !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================
# ABA 3 - HIPÓTESES DE SOLUÇÃO
# =========================

if aba_atual == t("tab_solutions"):

    st.title(t("tab_solutions"))

    st.markdown(
        f"""
<div style="
    font-size:24px;
    font-weight:500;
    color:#222;
    margin-top:-18px;
    margin-bottom:10px;
    opacity:0.92;
">
{t("solutions_subtitle")}
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("under_construction")}</div>
<div class="step-help">{t("solutions_construction_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )


# =========================
# ABA 4 - VIABILIDADE E IMPACTO
# =========================

if aba_atual == t("tab_viability"):

    st.title(t("tab_viability"))

    st.markdown(
        f"""
<div style="
    font-size:24px;
    font-weight:500;
    color:#222;
    margin-top:-18px;
    margin-bottom:10px;
    opacity:0.92;
">
{t("viability_subtitle")}
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="step-card">
<div class="step-title">{t("under_construction")}</div>
<div class="step-help">{t("viability_construction_help")}</div>
</div>
""",
        unsafe_allow_html=True
    )




st.markdown("""
<style>
@media (min-width: 769px) {
    div[role="radiogroup"] label {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    div[role="radiogroup"] label p {
        font-size: 18px !important;
        white-space: nowrap !important;
    }
}

@media (max-width: 768px) {
    div[role="radiogroup"] {
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
    }

    div[role="radiogroup"] label {
        flex: 0 0 auto !important;
        white-space: nowrap !important;
    }

    div[role="radiogroup"] label p {
        font-size: 15px !important;
        white-space: nowrap !important;
    }
}
</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>
/* AJUSTE FINO — HEADER FIXO COM 5 ABAS */
@media (min-width: 769px) {
    .fixed-workshop-header {
        top: 160px !important;
    }

    .fixed-workshop-header-spacer {
        height: 300px !important;
    }

    .timer-fixed-pill-global {
        top: 195px !important;
    }
}

@media (max-width: 768px) {
    .fixed-workshop-header {
        top: 195px !important;
    }

    .fixed-workshop-header-spacer {
        height: 390px !important;
    }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""<style>
@media (max-width: 768px) {
    .fixed-tabs-container button {
        min-width: 46% !important;
        flex: 1 1 46% !important;
    }
}
</style>""", unsafe_allow_html=True)


st.markdown("""<style>
/* MOBILE - 5 ABAS */
@media (max-width: 768px) {

    .fixed-tabs-container {
        display:flex !important;
        flex-wrap:wrap !important;
        gap:10px !important;
        align-items:flex-start !important;
    }

    .fixed-tabs-container button {
        white-space:nowrap !important;
        min-width:auto !important;
        flex:none !important;
        padding:12px 18px !important;
        font-size:15px !important;
    }
}
</style>""", unsafe_allow_html=True)



st.markdown("""
<style>

/* MOBILE - ORGANIZAÇÃO DAS 5 ABAS */
@media (max-width: 768px){

    .fixed-tabs-container{
        display:flex !important;
        flex-wrap:wrap !important;
        gap:10px !important;
    }

    .fixed-tabs-container button{
        width:auto !important;
        min-width:auto !important;
        flex:none !important;
        white-space:nowrap !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   AJUSTE VISUAL FINAL — BLOCO AZUL MAIS COMPACTO
   ========================================================= */

/* Blocos azuis de resultado, categorias, ranking e resumo */
.resultado-final-header {
    padding: 22px 24px !important;
    border-radius: 22px !important;
    margin-top: 14px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 22px rgba(0,47,95,0.16) !important;
}

.resultado-label {
    font-size: 13px !important;
    line-height: 1.25 !important;
    letter-spacing: 1.6px !important;
    margin-bottom: 8px !important;
}

.resultado-texto {
    font-size: 30px !important;
    line-height: 1.12 !important;
}

/* Header fixo azul menor no desktop */
@media (min-width: 769px) {
    .fixed-workshop-header {
        top: 138px !important;
        width: min(640px, calc(100vw - 360px)) !important;
        left: calc(50% - 105px) !important;
        transform: translateX(-50%) !important;
        padding: 0 !important;
        background: transparent !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }

    .fixed-workshop-header .header-foco {
        padding: 18px 24px !important;
        border-radius: 22px !important;
        margin-bottom: 0 !important;
        box-shadow: 0 10px 26px rgba(0,47,95,0.17) !important;
    }

    .fixed-workshop-header .header-title {
        font-size: 30px !important;
        line-height: 1.05 !important;
        margin-bottom: 6px !important;
    }

    .fixed-workshop-header .header-subtitle {
        font-size: 17px !important;
        line-height: 1.25 !important;
        font-weight: 650 !important;
    }

    .fixed-workshop-header-spacer {
        height: 220px !important;
    }

    .timer-fixed-pill-global {
        top: 150px !important;
    }
}

/* Mobile: mantém legível, mas um pouco mais compacto */
@media (max-width: 768px) {
    .resultado-final-header {
        padding: 18px 16px !important;
        border-radius: 20px !important;
        margin-top: 12px !important;
        margin-bottom: 18px !important;
    }

    .resultado-label {
        font-size: 11px !important;
        letter-spacing: 1.2px !important;
        margin-bottom: 7px !important;
    }

    .resultado-texto {
        font-size: 24px !important;
        line-height: 1.15 !important;
    }

    .fixed-workshop-header .header-foco {
        padding: 14px 16px !important;
        border-radius: 20px !important;
    }

    .fixed-workshop-header .header-title {
        font-size: 24px !important;
        line-height: 1.05 !important;
    }

    .fixed-workshop-header .header-subtitle {
        font-size: 15px !important;
        line-height: 1.2 !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   MOBILE — PRINCIPAIS ENTRAVES + HIPÓTESES LADO A LADO
   ========================================================= */
@media (max-width: 768px) {

    div[role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: stretch !important;
        justify-content: flex-start !important;
        gap: 6px !important;
    }

    div[role="radiogroup"] label {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: auto !important;
        max-width: none !important;
    }

    /* 3º botão = Principais Entraves | 4º botão = Hipóteses de Solução */
    div[role="radiogroup"] label:nth-child(3),
    div[role="radiogroup"] label:nth-child(4) {
        flex: 1 1 calc(50% - 6px) !important;
        max-width: calc(50% - 6px) !important;
        justify-content: center !important;
        text-align: center !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    div[role="radiogroup"] label:nth-child(3) p,
    div[role="radiogroup"] label:nth-child(4) p {
        width: 100% !important;
        text-align: center !important;
        white-space: normal !important;
        font-size: 14px !important;
        line-height: 1.05 !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   CORREÇÃO FINAL MOBILE — ABAS EM DUAS COLUNAS
   Garante Principais Entraves ao lado de Hipóteses de Solução
   ========================================================= */
@media (max-width: 768px) {

    div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: 1.35fr 1.35fr !important;
        column-gap: 3px !important;
        row-gap: 3px !important;
        align-items: stretch !important;
        justify-items: stretch !important;
        width: calc(100vw - 4px) !important;
        padding: 8px !important;
        box-sizing: border-box !important;
    }

    div[role="radiogroup"] label {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        flex: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        padding: 9px 7px !important;
        box-sizing: border-box !important;
        white-space: normal !important;
    }

    div[role="radiogroup"] label p {
        width: 100% !important;
        text-align: center !important;
        white-space: normal !important;
        font-size: 13px !important;
        line-height: 1.05 !important;
        font-weight: 850 !important;
    }

    /* Último botão ocupa uma linha mais elegante */
    div[role="radiogroup"] label:nth-of-type(5) {
        grid-column: 1 / span 2 !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   AJUSTE FINAL MOBILE — BOTÕES SEM QUEBRAR TEXTO
   ========================================================= */
@media (max-width: 768px) {

    div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: 1.35fr 1.35fr !important;
        gap: 10px !important;
    }

    div[role="radiogroup"] label {
        min-height: 72px !important;
        border-radius: 22px !important;
        padding: 10px 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[role="radiogroup"] label p {
        font-size: 13px !important;
        line-height: 1.15 !important;
        white-space: normal !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
        text-align: center !important;
    }

    /* Entraves + Hipóteses lado a lado */
    div[role="radiogroup"] label:nth-of-type(3),
    div[role="radiogroup"] label:nth-of-type(4) {
        min-height: 92px !important;
    }

    /* Viabilidade ocupa largura toda */
    div[role="radiogroup"] label:nth-of-type(5) {
        grid-column: 1 / span 2 !important;
        min-height: 70px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   CORREÇÃO DEFINITIVA MOBILE — ABAS 2x2 LEGÍVEIS
   ========================================================= */
@media (max-width: 768px) {

    /* container das abas */
    div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        gap: 3px !important;
        width: calc(100vw - 4px) !important;
        max-width: calc(100vw - 4px) !important;
        box-sizing: border-box !important;
        padding: 8px !important;
        align-items: stretch !important;
        justify-items: stretch !important;
    }

    /* cada botão */
    div[role="radiogroup"] label {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        height: 58px !important;
        min-height: 58px !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        padding: 8px 6px !important;
        border-radius: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        overflow: hidden !important;
        flex: none !important;
    }

    /* esconde a bolinha do radio no celular para liberar espaço */
    div[role="radiogroup"] label input,
    div[role="radiogroup"] label span:first-child,
    div[role="radiogroup"] label [data-testid="stWidgetLabel"] {
        display: none !important;
    }

    /* texto dos botões */
    div[role="radiogroup"] label p {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        hyphens: none !important;
        font-size: 13px !important;
        line-height: 1.08 !important;
        font-weight: 850 !important;
    }

    /* deixa a dupla crítica exatamente lado a lado e com altura boa */
    div[role="radiogroup"] label:nth-child(3),
    div[role="radiogroup"] label:nth-child(4),
    div[role="radiogroup"] label:nth-of-type(3),
    div[role="radiogroup"] label:nth-of-type(4) {
        height: 70px !important;
        min-height: 70px !important;
    }

    div[role="radiogroup"] label:nth-child(3) p,
    div[role="radiogroup"] label:nth-child(4) p,
    div[role="radiogroup"] label:nth-of-type(3) p,
    div[role="radiogroup"] label:nth-of-type(4) p {
        font-size: 12px !important;
        line-height: 1.08 !important;
    }

    /* último botão ocupa a largura toda */
    div[role="radiogroup"] label:nth-child(5),
    div[role="radiogroup"] label:nth-of-type(5) {
        grid-column: 1 / span 2 !important;
        height: 56px !important;
        min-height: 56px !important;
    }

    div[role="radiogroup"] label:nth-child(5) p,
    div[role="radiogroup"] label:nth-of-type(5) p {
        font-size: 13px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   MOBILE — ABAS MAIS BONITAS + HEADER MAIS BAIXO
   ========================================================= */
@media (max-width: 768px) {

    /* desce o bloco azul para não cortar */
    .fixed-workshop-header {
        top: 245px !important;
    }

    .fixed-workshop-header-spacer {
        height: 320px !important;
    }

    /* botões */
    div[role="radiogroup"] label:nth-child(3),
    div[role="radiogroup"] label:nth-child(4),
    div[role="radiogroup"] label:nth-of-type(3),
    div[role="radiogroup"] label:nth-of-type(4) {

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        height: 72px !important;
        min-height: 72px !important;

        border-radius: 24px !important;

        padding: 10px 14px !important;

        overflow: hidden !important;
    }

    div[role="radiogroup"] label:nth-child(3) p,
    div[role="radiogroup"] label:nth-child(4) p,
    div[role="radiogroup"] label:nth-of-type(3) p,
    div[role="radiogroup"] label:nth-of-type(4) p {

        font-size: 12px !important;
        line-height: 1.15 !important;

        white-space: normal !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;

        text-align: center !important;

        max-width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   MOBILE FINAL — ABAS ESTÁVEIS, SEM BUG AO CLICAR
   ========================================================= */
@media (max-width: 768px) {

    /* Container geral das abas */
    div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;

        width: calc(100vw - 20px) !important;
        max-width: calc(100vw - 20px) !important;

        padding: 8px !important;
        box-sizing: border-box !important;

        align-items: stretch !important;
        justify-items: stretch !important;
    }

    /* Todos os botões em estado normal e selecionado */
    div[role="radiogroup"] label,
    div[role="radiogroup"] label:has(input:checked),
    div[role="radiogroup"] label:nth-child(3),
    div[role="radiogroup"] label:nth-child(4),
    div[role="radiogroup"] label:nth-child(5),
    div[role="radiogroup"] label:nth-of-type(3),
    div[role="radiogroup"] label:nth-of-type(4),
    div[role="radiogroup"] label:nth-of-type(5) {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;

        height: 74px !important;
        min-height: 74px !important;

        padding: 10px 8px !important;
        margin: 0 !important;
        box-sizing: border-box !important;

        border-radius: 20px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        text-align: center !important;
        overflow: hidden !important;

        flex: unset !important;
        grid-column: auto !important;
    }

    /* A linha que você queria: Entraves + Hipóteses lado a lado */
    div[role="radiogroup"] label:nth-child(3),
    div[role="radiogroup"] label:nth-child(4),
    div[role="radiogroup"] label:nth-of-type(3),
    div[role="radiogroup"] label:nth-of-type(4) {
        height: 82px !important;
        min-height: 82px !important;
    }

    /* Último botão ocupa a largura inteira */
    div[role="radiogroup"] label:nth-child(5),
    div[role="radiogroup"] label:nth-of-type(5) {
        grid-column: 1 / span 2 !important;
        height: 66px !important;
        min-height: 66px !important;
    }

    /* Texto sempre controlado, inclusive selecionado */
    div[role="radiogroup"] label p,
    div[role="radiogroup"] label:has(input:checked) p,
    div[role="radiogroup"] label:nth-child(3) p,
    div[role="radiogroup"] label:nth-child(4) p,
    div[role="radiogroup"] label:nth-child(5) p,
    div[role="radiogroup"] label:nth-of-type(3) p,
    div[role="radiogroup"] label:nth-of-type(4) p,
    div[role="radiogroup"] label:nth-of-type(5) p {
        width: 100% !important;
        max-width: 100% !important;

        margin: 0 !important;
        padding: 0 !important;

        text-align: center !important;

        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        hyphens: none !important;

        font-size: 13px !important;
        line-height: 1.12 !important;
        font-weight: 850 !important;
    }

    /* Dá um pouco mais de respiro nos textos longos */
    div[role="radiogroup"] label:nth-child(3) p,
    div[role="radiogroup"] label:nth-child(4) p,
    div[role="radiogroup"] label:nth-of-type(3) p,
    div[role="radiogroup"] label:nth-of-type(4) p {
        font-size: 12.5px !important;
        line-height: 1.12 !important;
    }

    /* Bolinha do rádio: menor e sem roubar layout */
    div[role="radiogroup"] label > div:first-child {
        margin-right: 4px !important;
        flex: 0 0 auto !important;
        transform: scale(0.82) !important;
    }

    /* Evita que Streamlit mude largura quando seleciona */
    div[role="radiogroup"] label:has(input:checked) {
        transform: none !important;
    }

    /* Header azul desce um pouco e não é coberto */
    .fixed-workshop-header {
        top: 245px !important;
        width: calc(100vw - 20px) !important;
    }

    .fixed-workshop-header-spacer {
        height: 330px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* Garante que as abas reapareçam quando o cabeçalho estiver ativo */
body:not(.hide-fixed-header) div[role="radiogroup"]{
    visibility: visible !important;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   MOBILE — RESUMO MAIS BAIXO + ABAS OCULTÁVEIS
   ========================================================= */
@media (max-width: 768px) {

    .summary-mobile-spacer {
        height: 150px !important;
    }

    /* Cabeçalho normal da aba Resumo mais baixo/sem corte */
    .header-foco {
        margin-top: 18px !important;
    }
}
</style>
""", unsafe_allow_html=True)



if st.session_state.get("esconder_cabecalho_fixo", False):

    st.markdown(
        """
<style>
@media (max-width: 768px) {
    .summary-mobile-spacer {
        height: 16px !important;
    }
}
</style>
""",
        unsafe_allow_html=True
    )



st.markdown("""
<style>
/* =========================================================
   MOBILE — ESPAÇO ANTES DO HEADER DO RESUMO
   ========================================================= */
@media (max-width: 768px) {
    .summary-header-mobile-spacer {
        height: 165px !important;
        min-height: 165px !important;
    }
}
</style>
""", unsafe_allow_html=True)

if st.session_state.get("esconder_cabecalho_fixo", False):

    st.markdown(
        """
<style>
@media (max-width: 768px) {
    .summary-header-mobile-spacer {
        height: 16px !important;
        min-height: 16px !important;
    }
}
</style>
""",
        unsafe_allow_html=True
    )





st.markdown("""
<style>
/* =========================================================
   PROVA DE STREAMLIT — TIMER MOBILE CENTRALIZADO
   ========================================================= */
@media (max-width: 768px) {
    .timer-mobile-stack {
        margin-top: -52px !important;
        margin-bottom: 8px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
    }

    .timer-mobile-stack .timer-status-top {
        order: 1 !important;
        color: #24476b !important;
        font-size: 17px !important;
        line-height: 1.15 !important;
        font-weight: 850 !important;
        text-align: center !important;
        margin: 0 0 8px 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    .timer-mobile-stack .timer-display-mobile {
        order: 2 !important;
        color: #002f5f !important;
        font-size: 52px !important;
        line-height: 0.95 !important;
        font-weight: 950 !important;
        text-align: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    /* reduz espaço depois do relógio para o conjunto parecer centralizado */
    .st-key-timer_area_foco_no_foco,
    .st-key-timer_area_principais_entraves {
        margin-bottom: -10px !important;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* =========================================================
   CORREÇÃO REAL MOBILE — CRONÔMETRO E CABEÇALHO
   ========================================================= */
@media (max-width: 768px) {

    .timer-mobile-row {
        margin-top: -18px !important;
        margin-bottom: 10px !important;
    }

    .timer-mobile-info {
        min-height: 108px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        padding-top: 0 !important;
    }

    .timer-mobile-label {
        color: #24476b !important;
        font-size: 17px !important;
        line-height: 1.15 !important;
        font-weight: 850 !important;
        margin-bottom: 8px !important;
        text-align: center !important;
    }

    .timer-mobile-time {
        color: #002f5f !important;
        font-size: 54px !important;
        line-height: 0.95 !important;
        font-weight: 950 !important;
        text-align: center !important;
    }

    /* relógio alinhado ao centro do bloco */
    .st-key-timer_area_foco_no_foco .stButton > button,
    .st-key-timer_area_principais_entraves .stButton > button {
        margin-left: 0 !important;
        margin-top: 6px !important;
        margin-right: auto !important;
    }
}

/* Quando esconder cabeçalho, mata qualquer sobra visual das abas/header */
@media (max-width: 768px) {
    div[role="radiogroup"][style*="display: none"],
    .fixed-workshop-header[style*="display: none"] {
        display: none !important;
    }
}
</style>
""", unsafe_allow_html=True)
