# app/main.py
from fastapi import FastAPI

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title="CineTrack API",
    description="Backend para gerenciamento de catálogo pessoal de filmes.",
    version="0.1.0"
)

# Rota principal (Hello World)
@app.get("/")
def read_root():
    return {
        "status": "sucesso",
        "mensagem": "Olá, Mundo! O backend do CineTrack está no ar e pronto para receber HTMX!"
    }

# Rota de teste para ver como o FastAPI devolve dados
@app.get("/ping")
def ping():
    return {"ping": "pong"}


"""
uvicorn main:app --reload

O Uvicorn é o "motor" que vai rodar o FastAPI.
O --reload faz com que o servidor atualize sozinho toda vez que você salvar o arquivo (ótimo para desenvolver).
"""