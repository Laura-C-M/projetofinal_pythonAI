import streamlit as st
import os
import json
from dotenv import load_dotenv
from gemini import configurar_gemini, gerar_recomendacoes
from tmdb import configurar_tmdb, buscar_tmdb
 
ARQUIVO_RECOMENDACOES = "recomendacoes.json"
 
# ------------------ JSON ------------------
#serve para cfriar o ficheiro JSON onde as informações ficam guardadas
 
def inicializar_json():
    if not os.path.exists(ARQUIVO_RECOMENDACOES):
        with open(ARQUIVO_RECOMENDACOES, "w", encoding="utf-8") as f:
            json.dump({"recomendacoes": [], "favoritos": []}, f, indent=2, ensure_ascii=False)
#inicia o código com as recomendações vazias
 
def carregar_dados():
    with open(ARQUIVO_RECOMENDACOES, "r", encoding="utf-8") as f:
        return json.load(f)
#carrega os dados do código 
 
def guardar_recomendacoes(filmes):
    dados = carregar_dados()
    dados["recomendacoes"] = filmes
    with open(ARQUIVO_RECOMENDACOES, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
#guarda as recomendações feitas
 
def adicionar_favorito(filme):
    dados = carregar_dados()
    if filme not in dados["favoritos"]:
        dados["favoritos"].append(filme)
    with open(ARQUIVO_RECOMENDACOES, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
#coloca o filme como guardado nos favoritos
 
# ------------------ INIT ------------------
 
st.set_page_config(
    page_title="Recomendador de Filmes",
    page_icon="🎬"
)
 
inicializar_json()
load_dotenv()
 
gemini_key = os.getenv("GEMINI_API_KEY")
tmdb_key = os.getenv("TMDB_API_KEY")
 
if not gemini_key or not tmdb_key:
    st.error("Configure GEMINI_API_KEY e TMDB_API_KEY no .env")
    st.stop()
 
model = configurar_gemini(gemini_key)
 
idioma = st.selectbox("Idioma / Language", ["pt-PT", "en-US"])
configurar_tmdb(tmdb_key, idioma)
 
dados = carregar_dados()
st.session_state.setdefault("favoritos", dados.get("favoritos", []))
 
# ------------------ UI ------------------
 
st.title("🎬 Recomendador de Filmes com IA")
st.write("Gemini 2.5 + TMDb")
 
with st.form("form_filmes"):
    genero = st.text_input("Género favorito")
    epoca = st.selectbox("Época", ["Não importa", "Antes de 2000", "Depois de 2010"])
    estilo = st.radio("Estilo", ["Leve", "Emocional", "Equilibrado"])
    quantidade = st.slider("Quantidade", 3, 10, 5)
    submeter = st.form_submit_button("Gerar recomendações")
 
# ------------------ AÇÃO ------------------
 
if submeter:
    preferencias = {
        "genero": genero,
        "epoca": epoca,
        "estilo": estilo
    }
 
    with st.spinner("A gerar recomendações..."):
        filmes = gerar_recomendacoes(model, preferencias, quantidade)
        guardar_recomendacoes(filmes)
 
    for filme in filmes:
        with st.expander(f"{filme['title']} ({filme['year']})"):
            col1, col2 = st.columns([1, 2])
 
            with col1:
                dados_tmdb = buscar_tmdb(filme["title"], filme["year"])
                if dados_tmdb.get("poster"):
                    st.image(dados_tmdb["poster"], width=200)
 
            with col2:
                st.write(filme["description"])
                st.write(f"⭐ {filme['rating']}/10")
 
                if dados_tmdb.get("trailer"):
                    st.video(dados_tmdb["trailer"])
 
                if st.button(f"Adicionar aos favoritos – {filme['title']}"):
                    adicionar_favorito(filme)
                    st.success("Adicionado aos favoritos!")
 
# ------------------ FAVORITOS ------------------
 
if st.session_state["favoritos"]:
    with st.expander("⭐ Filmes Favoritos"):
        for f in st.session_state["favoritos"]:
            st.write(f"{f['title']} ({f['year']}) – {f['rating']}/10")