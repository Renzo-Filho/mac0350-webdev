# app/tmdb.py
import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env pro Python
load_dotenv()

# Pega o token gigante do cofre
TMDB_READ_TOKEN = os.getenv("TMDB_READ_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"

def buscar_filmes(query: str):
    """Busca filmes no TMDb de forma segura usando o Read Access Token"""
    url = f"{BASE_URL}/search/movie"
    
    # Parâmetros da busca (idioma e o texto digitado)
    params = {
        "query": query,
        "language": "pt-BR",
        "include_adult": False
    }
    
    # O cabeçalho onde o token vai "escondido"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_READ_TOKEN}"
    }
    
    # Fazendo a requisição juntando a URL, os parâmetros e o cabeçalho seguro
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        dados = response.json()
        return dados.get("results", [])
    
    return []