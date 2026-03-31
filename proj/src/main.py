from fastapi import FastAPI, Request, Form, HTTPException, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from typing import Optional
from sqlmodel import Session, select, or_
from src.models import Usuario
from src.db import engine, criar_banco_e_tabelas
from src.services.tmdb import buscar_filmes, buscar_detalhes_filme, buscar_lancamentos, buscar_tendencias
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # antes do 'yield' roda na hora que o servidor LIGA
    print("Iniciando o servidor e verificando o banco de dados...")
    criar_banco_e_tabelas()
    
    yield
    
    # depois do 'yield' roda quando o servidor DESLIGA 
    print("Desligando o servidor...")

app = FastAPI(
    title="HelloMovie API",
    description="Backend para gerenciamento de catálogo pessoal de filmes.",
    version="0.1.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def helloMovie(request: Request, usuario_id: Optional[str] = Cookie(default=None)):
    usuario = None
    if usuario_id:
        with Session(engine) as session:
            usuario = session.get(Usuario, int(usuario_id))

    tendencias = buscar_tendencias()
    lancamentos = buscar_lancamentos()
    
    context = {
        "request": request,
        "usuario": usuario, 
        "carrossel": tendencias[:5],    
        "sugestoes": tendencias[5:11],  
        "lancamentos": lancamentos[:6] 
    }

    return templates.TemplateResponse("index.html", context)

@app.get("/buscar")
def buscar(request: Request, query: str = ""):
    if not query:
        return templates.TemplateResponse("resultadosBusca.html", {"request": request, "filmes": []})
    
    filmes_encontrados = buscar_filmes(query)
    context = {
        "request": request,
        "filmes": filmes_encontrados
    }

    return templates.TemplateResponse("resultadosBusca.html", context)

@app.get("/filme/{filme_id}")
def detalhesFilme(request: Request, filme_id: int):
    filme = buscar_detalhes_filme(filme_id)

    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    context = {
        "request": request,
        "filme": filme
    }

    return templates.TemplateResponse("filmeDetalhes.html", context)

@app.get("/login")
def paginaLogin(request: Request):
    filmes_fundo = buscar_tendencias()

    context = {
        "request": request,
        "filmes": filmes_fundo
    }

    return templates.TemplateResponse("login.html", context)
    
@app.post("/login")
def logar(request: Request, nome_ou_email: str = Form(...), senha: str = Form(...)):
    
    with Session(engine) as session:

        verificar_nome_ou_email = select(Usuario).where(
            or_(Usuario.nome_usuario == nome_ou_email, Usuario.email == nome_ou_email))
        
        usuario = session.exec(verificar_nome_ou_email).first()
        
        if not usuario or not pwd_context.verify(senha, usuario.senha):
            filmes_fundo = buscar_tendencias()
            context = {"request": request, "erro": "Usuário ou senha incorretos!", "filmes": filmes_fundo}

            return templates.TemplateResponse("login.html", context)
        
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="usuario_id", value=str(usuario.id), max_age=86400)

        return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("usuario_id")
    
    return response

@app.get("/cadastro")
def paginaCadastro(request: Request):

    filmes_fundo = buscar_tendencias()

    context = {
        "request": request,
        "filmes": filmes_fundo
    }

    return templates.TemplateResponse("cadastro.html", context)

@app.post("/cadastro")
def cadastrar(request: Request, nome: str = Form(...), email: str = Form(...), senha: str = Form(...)):

    with Session(engine) as session:
        usuario_nome = session.exec(select(Usuario).where(Usuario.nome_usuario == nome)).first()
        usuario_email = session.exec(select(Usuario).where(Usuario.email == email)).first()
        
        filmes_fundo = buscar_tendencias()

        if usuario_email:
            context = {"request": request, "erro": "Esse email já está em uso!", "filmes": filmes_fundo}
            return templates.TemplateResponse("cadastro.html", context)
        
        if usuario_nome:
            context2 = {"request": request, "erro": "Esse nome de usuário já está em uso!",  "filmes": filmes_fundo}
            return templates.TemplateResponse("cadastro.html", context2)
        
        senha_hash = pwd_context.hash(senha)
        
        novo_usuario = Usuario(nome_usuario=nome, email=email, senha=senha_hash)
        session.add(novo_usuario)
        session.commit()
        
        return RedirectResponse(url="/login", status_code=303)

@app.get("/perfil")
def paginaPerfil(request: Request, usuario_id: Optional[str] = Cookie(default=None)):
    if not usuario_id:
        return RedirectResponse(url="/", status_code=303)
    
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        
        if not usuario:
            return RedirectResponse(url="/", status_code=303)
            
    context = {
        "request": request,
        "usuario": usuario
    }
    
    return templates.TemplateResponse("perfil.html", context)

"""
uvicorn main:app --reload

O Uvicorn é o "motor" que vai rodar o FastAPI.
O --reload faz com que o servidor atualize sozinho toda vez que você salvar o arquivo (ótimo para desenvolver).
"""