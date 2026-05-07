import streamlit as st
import time
import sqlite3

st.set_page_config(page_title="Foco no Foco", layout="centered")

# Banco de dados
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


# FOCO FORA DAS ABAS


st.subheader("Foco")

foco = st.text_input(
    " ",
    placeholder="Digite aqui o título do foco"
)

st.divider()


aba1, aba2 = st.tabs(["Foco no Foco", "Principais Obstáculos"])


with aba1:
    st.title("Foco no Foco")
    st.subheader("Cadastro da Equipe")

    nome_equipe = st.text_input(
        "Nome da equipe",
        placeholder="Digite o nome da equipe"
    )

    lider_equipe = st.text_input(
        "Líder da equipe",
        placeholder="Digite o nome do líder"
    )

    st.divider()

    tempo_total = 60

    if "inicio_timer" not in st.session_state:
        st.session_state.inicio_timer = None

    if st.button("Iniciar cronômetro de 1 minuto"):
        st.session_state.inicio_timer = time.time()

    if st.session_state.inicio_timer:
        tempo_passado = int(time.time() - st.session_state.inicio_timer)
        tempo_restante = max(tempo_total - tempo_passado, 0)

        st.markdown(f"## ⏱️ {tempo_restante} segundos restantes")
        st.progress(tempo_restante / tempo_total)

        if tempo_restante > 0:
            time.sleep(1)
            st.rerun()
        else:
            st.error("Tempo encerrado!")

    st.divider()

    st.subheader("Post-its das equipes")

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
            st.warning("Preencha o nome da equipe antes de adicionar um post-it.")

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

    st.divider()

    cursor.execute("SELECT equipe, texto FROM postits ORDER BY id DESC")
    postits = cursor.fetchall()

    if postits:
        colunas = st.columns(3)

        for i, (equipe, texto) in enumerate(postits):
            with colunas[i % 3]:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #fff3a3;
                        padding: 20px;
                        border-radius: 8px;
                        min-height: 160px;
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
                        margin-bottom: 20px;
                        color: #1f2937;
                        font-family: Arial, sans-serif;
                        overflow-wrap: break-word;
                        word-break: normal;
                        white-space: normal;
                    ">
                        <h4 style="
                            margin-top: 0;
                            margin-bottom: 12px;
                            font-size: 18px;
                            line-height: 1.2;
                            overflow-wrap: break-word;
                            word-break: normal;
                            white-space: normal;
                        ">
                            {equipe}
                        </h4>

                        <p style="
                            font-size: 18px;
                            font-weight: 600;
                            line-height: 1.35;
                            margin: 0;
                            overflow-wrap: break-word;
                            word-break: normal;
                            white-space: normal;
                        ">
                            {texto}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:
        st.info("Nenhum post-it adicionado ainda.")


with aba2:
    st.subheader("Principais Obstáculos")

    st.info("Essa aba está reservada para a próxima etapa.")
