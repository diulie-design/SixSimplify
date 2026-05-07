import streamlit as st
import time

st.set_page_config(page_title="Foco no Foco", layout="centered")

st.title("Foco no Foco")

foco = st.text_input(
    "Foco",
    placeholder="Digite aqui o título do foco"
)

st.subheader("Dados da equipe")

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

    progresso = tempo_restante / tempo_total
    st.progress(progresso)

    if tempo_restante > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.error("Tempo encerrado!")

st.divider()

if st.button("Confirmar dados"):
    st.success("Dados registrados!")

    st.write("**Foco:**", foco)
    st.write("**Equipe:**", nome_equipe)
    st.write("**Líder:**", lider_equipe)
