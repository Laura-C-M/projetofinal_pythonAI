from tmdbv3api import TMDb, Movie
 
tmdb = TMDb()
movie_api = Movie()
 
def configurar_tmdb(api_key, idioma="pt-PT"):
    tmdb.api_key = api_key
    tmdb.language = idioma
 
def buscar_tmdb(titulo, ano):
    try:
        resultados = movie_api.search(titulo)
 
        for filme in resultados:
            # Garantir release_date válida
            if not hasattr(filme, "release_date") or not filme.release_date:
                continue
 
            try:
                ano_filme = int(filme.release_date[:4])
            except ValueError:
                continue
 
            # Aceita variação de ano ±1
            if abs(ano_filme - ano) > 1:
                continue
 
            detalhes = movie_api.details(filme.id)
 
            # Buscar trailers
            trailer = None
            try:
                videos = movie_api.videos(filme.id)
            except Exception:
                videos = []
 
            for video in videos:
                # video pode ser string
                if not hasattr(video, "site"):
                    continue
 
                if video.site == "YouTube" and video.type == "Trailer":
                    trailer = video.key
                    break
 
            return {
                "poster": (
                    f"https://image.tmdb.org/t/p/w500{detalhes.poster_path}"
                    if getattr(detalhes, "poster_path", None)
                    else None
                ),
                "trailer": (
                    f"https://www.youtube.com/embed/{trailer}"
                    if trailer
                    else None
                )
            }
 
        return {}
 
    except Exception as e:
        print(f"Erro ao buscar no TMDb: {e}")
        return {}