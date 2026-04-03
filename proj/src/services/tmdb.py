import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_READ_TOKEN = os.getenv("TMDB_READ_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"

def buscar_filmes(query: str):
    url = f"{BASE_URL}/search/movie"
    
    params = {
        "query": query,
        "language": "pt-BR",
        "include_adult": False
    }
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_READ_TOKEN}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        dados = response.json()
        return dados.get("results", [])
    
    return []

def buscar_detalhes_filme(filme_id: int):
    url = f"{BASE_URL}/movie/{filme_id}"
    
    params = {
        "language": "pt-BR",
        "append_to_response": "credits" 
    }
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_READ_TOKEN}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    
    return None

def buscar_tendencias():
    url = f"{BASE_URL}/trending/movie/week"
    params = {"language": "pt-BR"}
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_READ_TOKEN}"}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    
    return []

def buscar_lancamentos():
    url = f"{BASE_URL}/movie/now_playing"
    params = {"language": "pt-BR", "region": "BR"} 
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_READ_TOKEN}"}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    
    return []