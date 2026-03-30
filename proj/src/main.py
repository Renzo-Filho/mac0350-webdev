# app/main.py
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.db import criar_banco_e_tabelas
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tudo que está antes do 'yield' roda na hora que o servidor LIGA
    print("Iniciando o servidor e verificando o banco de dados...")
    criar_banco_e_tabelas()
    
    yield # O servidor fica rodando aqui
    
    # Tudo que está depois do 'yield' roda quando o servidor DESLIGA (CTRL+C)
    print("Desligando o servidor do HelloMovie...")

app = FastAPI(
    title="HelloMovie API",
    description="Backend para gerenciamento de catálogo pessoal de filmes.",
    version="0.1.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def helloMovie(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/login")
def login():
    pass

@app.post("/login")
def login2():
    pass



"""
uvicorn main:app --reload

O Uvicorn é o "motor" que vai rodar o FastAPI.
O --reload faz com que o servidor atualize sozinho toda vez que você salvar o arquivo (ótimo para desenvolver).
"""