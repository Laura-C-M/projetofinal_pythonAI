# =====================

# 1. IMPORTS / IMPORTAÇÕES

# =====================

 

import streamlit as st  # Web interface library / Biblioteca para interfaces web

import google as genai  # Google Gemini AI SDK / SDK da IA Gemini do Google

import os  # Environment variables / Variáveis de ambiente

import json  # JSON parsing / Manipulação de JSON

from tmdbv3api import TMDb, Movie  # TMDb API SDK / Biblioteca oficial TMDb

 

# =====================

# 2. API KEYS CONFIG / CONFIGURAÇÃO DAS CHAVES

# =====================

 

# Try to get API keys from Streamlit Secrets first / Tenta obter chaves do Streamlit Secrets

# If not, use environment variables / Caso contrário, usa variáveis de ambiente

gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

tmdb_key = st.secrets.get("TMDB_API_KEY") or os.getenv("TMDB_API_KEY")

 

# Stop execution if keys are missing / Para o programa se chaves estiverem ausentes

if not gemini_key or not tmdb_key:

    st.error("É necessário configurar GEMINI_API_KEY e TMDB_API_KEY / GEMINI_API_KEY and TMDB_API_KEY must be set")

    st.stop()

 

# =====================

# 3. GEMINI AI CONFIG / CONFIGURAÇÃO GEMINI (IA)

# =====================

 

genai.configure(api_key=gemini_key)  # Configure SDK with API key / Configura SDK com a chave

model = genai.GenerativeModel("gemini-1.5-flash")  # Model selection / Seleção do modelo

 

# =====================

# 4. TMDb CONFIG / CONFIGURAÇÃO TMDb

# =====================

 

tmdb = TMDb()  # TMDb configuration object / Objeto de configuração TMDb

tmdb.api_key = tmdb_key  # API key / Chave da API

tmdb.language = "pt-PT"  # Result language / Idioma dos resultados

movie_api = Movie()  # Movie endpoint / Endpoint para filmes

 

# =====================

# 5. FUNCTION: GENERATE MOVIES WITH GEMINI / FUNÇÃO: GERAR FILMES COM GEMINI

# =====================

 

def gerar_recomendacoes(preferencias, quantidade):

    """Generate movie recommendations via Gemini AI / Gera recomendações de filmes via IA"""

 

    prompt = f"""

    Baseado nas preferências abaixo, sugira exatamente {quantidade} filmes. / Based on preferences below, suggest exactly {quantidade} movies.

 

    Preferências / Preferences:

    {json.dumps(preferencias, ensure_ascii=False)}

 

    Responda EXCLUSIVAMENTE em JSON no formato / Respond EXCLUSIVELY in JSON format:

    [

      {{

        "title": "Movie title / Título do filme",

        "year": 2020,

        "description": "Short description / Descrição curta",

        "rating": 8

      }}

    ]

    """

 

    try:

        resposta = model.generate_content(prompt)  # Send prompt to Gemini / Envia prompt

        filmes = json.loads(resposta.text)  # Parse JSON response / Parse JSON

        return filmes

 

    except Exception as erro:

        raise RuntimeError(f"Erro ao gerar recomendações / Error generating recommendations: {erro}")

 

# =====================

# 6. FUNCTION: FETCH TMDb DATA / FUNÇÃO: BUSCAR DADOS NO TMDb

# =====================

 

def buscar_tmdb(titulo, ano):

    resultados = movie_api.search(titulo)  # Search movie / Pesquisa filme

 

    for filme in resultados:

        if filme.release_date:

            if abs(int(filme.release_date[:4]) - ano) <= 1:  # Year check / Verifica ano

                detalhes = movie_api.details(filme.id)  # Movie details / Detalhes

                videos = movie_api.videos(filme.id)  # Movie videos / Vídeos do filme

 

                trailer = None

                for video in videos:

                    if video.site == "YouTube" and video.type == "Trailer":

                        trailer = video.key

                        break

 

                return {

                    "poster": f"https://image.tmdb.org/t/p/w500{detalhes.poster_path}" if detalhes.poster_path else None,

                    "trailer": f"https://www.youtube.com/embed/{trailer}" if trailer else None

                }

 

    return {}  # Return empty if not found / Retorna vazio se não encontrado

 

# =====================

# 7. STREAMLIT INTERFACE / INTERFACE STREAMLIT

# =====================

 

st.set_page_config(page_title="Recomendador de Filmes / Film Recommender", page_icon="🎬")

st.title("🎬 Recomendador de Filmes com IA / Film Recommender with AI")

st.write("Aplicação educativa usando Gemini + TMDb / Educational app using Gemini + TMDb")

 

with st.form("form_filmes"):

    genero = st.text_input("Género favorito / Favorite genre")

    epoca = st.selectbox("Época / Era", ["Não importa / Not important", "Antes de 2000 / Before 2000", "Depois de 2010 / After 2010"])

    estilo = st.radio("Estilo do filme / Movie style", ["Leve / Light", "Emocional / Emotional", "Equilibrado / Balanced"])

    quantidade = st.slider("Quantidade de filmes / Number of movies", 3, 10, 5)

 

    submeter = st.form_submit_button("Gerar filmes / Generate movies")

 

if submeter:

    preferencias = {"genero": genero, "epoca": epoca, "estilo": estilo}

 

    with st.spinner("A gerar recomendações... / Generating recommendations..."):

        filmes = gerar_recomendacoes(preferencias, quantidade)

 

    for filme in filmes:

        with st.expander(f"{filme['title']} ({filme['year']})"):

            st.write(filme["description"])

            st.write(f"Nota / Rating: {filme['rating']}/10")

 

            dados_tmdb = buscar_tmdb(filme["title"], filme["year"])

 

            if dados_tmdb.get("poster"):

                st.image(dados_tmdb["poster"], width=250)

 

            if dados_tmdb.get("trailer"):

                st.video(dados_tmdb["trailer"])

 

# =====================

# 8. EXTRA CHALLENGES / DESAFIOS EXTRA PARA OS ALUNOS

# =====================

 

# 1️⃣ Save recommendations to JSON file / Guardar recomendações num ficheiro JSON

# 2️⃣ Add language selection / Adicionar escolha de idioma

# 3️⃣ Show trailers only on button click / Mostrar trailers só ao clicar no botão

# 4️⃣ Limit API calls / Limitar chamadas à API

# 5️⃣ Create favorites system / Criar sistema de favoritos

# 6️⃣ Improve UI design / Melhorar design visual

# ==================================================
