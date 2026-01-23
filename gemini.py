from google import genai #importa o gemini como IA do programa
import json #importa a parte json do código
 
 #Funçoes

def configurar_gemini(api_key):
    return genai.Client(api_key=api_key)
#usa a API key para ter acesso à IA usada no código
 
def gerar_recomendacoes(client, preferencias, quantidade):
    prompt = f"""
Baseado nas preferências abaixo, sugira exatamente {quantidade} filmes.
 
Preferências:
{json.dumps(preferencias, ensure_ascii=False)}
 
Formato esperado:
[
  {{
    "title": "Título",
    "year": 2020,
    "description": "Descrição curta",
    "rating": 8
  }}
]
"""
#mostra as preferencias escolhidas pelo o utilizador e armazenadas no json
 
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
 
        # Agora o Gemini é OBRIGADO a devolver JSON puro
        filmes = json.loads(response.text)
 
        if not isinstance(filmes, list):
            raise ValueError("Resposta não é uma lista de filmes")
 
        return filmes
 
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Erro ao decodificar JSON do Gemini.\nResposta recebida:\n{response.text}"
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar recomendações: {e}")