from fastapi import FastAPI, Request, Form, HTTPException, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from typing import Optional
from sqlmodel import Session, select, or_
from src.models import Usuario, Filme, ListaUsuario
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
def detalhesFilme(request: Request, filme_id: int, usuario_id: Optional[str] = Cookie(default=None)):
    usuario = None
    relacao_usuario_filme = None
    avaliacoes = [] 
    
    with Session(engine) as session:
        if usuario_id:
            usuario = session.get(Usuario, int(usuario_id))

        filme_db = session.exec(select(Filme).where(Filme.tmdb_id == filme_id)).first()

        if filme_db:
            if usuario:
                relacao_usuario_filme = session.exec(select(ListaUsuario).where(
                    ListaUsuario.usuario_id == usuario.id,
                    ListaUsuario.filme_id == filme_db.id
                )).first()
            
            # query de busca por todos os comentários
            query = select(ListaUsuario, Usuario).join(Usuario).where(
                ListaUsuario.filme_id == filme_db.id,
                ListaUsuario.comentario != None,
                ListaUsuario.comentario != ""
            )
            avaliacoes = session.exec(query).all()

    filme = buscar_detalhes_filme(filme_id)

    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    context = {
        "request": request,
        "filme": filme,
        "usuario": usuario,
        "relacao": relacao_usuario_filme,
        "avaliacoes": avaliacoes
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
        return RedirectResponse(url="/login", status_code=303)
    
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        
        if not usuario:
            return RedirectResponse(url="/login", status_code=303)
    
        minha_lista = session.exec(select(ListaUsuario).where(ListaUsuario.usuario_id == usuario.id)).all()

        total_filmes = len(minha_lista)
        total_avaliacoes = sum(1 for item in minha_lista if item.nota is not None)
            
    context = {
        "request": request,
        "usuario": usuario,
        "total_filmes": total_filmes,        
        "total_avaliacoes": total_avaliacoes
    }
    
    return templates.TemplateResponse("perfil.html", context)

@app.get("/minhaLista")
def paginaMinhaLista(request: Request, status: Optional[str] = None, usuario_id: Optional[str] = Cookie(default=None)):
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=303)
    
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        
        if not usuario:
            return RedirectResponse(url="/login", status_code=303)
        
        query = select(Filme, ListaUsuario).join(ListaUsuario).where(ListaUsuario.usuario_id == usuario.id)
        
        if status and status != "Todos":
            query = query.where(ListaUsuario.status == status)
            
        meus_filmes = session.exec(query).all() 
        
    context = {
        "request": request,
        "usuario": usuario,
        "filmes": meus_filmes,
        "status_atual": status or "Todos"
    }

    return templates.TemplateResponse("minhaLista.html", context)

@app.post("/minhaLista/adicionar/{tmdb_id}")
def adicionarLista(request: Request, tmdb_id: int, status: str = Form(...), nota: Optional[int] = Form(None), 
                   comentario: Optional[str] = Form(None), usuario_id: Optional[str] = Cookie(default=None)):
    
    if not usuario_id:
        response = HTMLResponse("")
        response.headers["HX-Redirect"] = "/login"
        return response
        
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        if not usuario:
            response = HTMLResponse("")
            response.headers["HX-Redirect"] = "/login"
            return response
            
        existe_filme_db = session.exec(select(Filme).where(Filme.tmdb_id == tmdb_id)).first()
        if not existe_filme_db:
            dados_tmdb = buscar_detalhes_filme(tmdb_id)
            if not dados_tmdb:
                return HTMLResponse("<span class='text-red-500'>Erro ao buscar filme!</span>")
            
            existe_filme_db = Filme(
                tmdb_id=tmdb_id, titulo=dados_tmdb.get("title", "Sem Título"),
                sinopse=dados_tmdb.get("overview", ""), poster_url=dados_tmdb.get("poster_path", ""),
                data_lancamento=dados_tmdb.get("release_date", "")
            )
            session.add(existe_filme_db)
            session.commit()
            session.refresh(existe_filme_db)
        
        filme_esta_na_lista = session.exec(select(ListaUsuario).where(
            ListaUsuario.usuario_id == usuario.id, 
            ListaUsuario.filme_id == existe_filme_db.id
        )).first()
        
        if filme_esta_na_lista:
            return HTMLResponse("""
                <div id="modal-content" class="bg-surface border border-gray-800 rounded-xl p-8 shadow-2xl w-full max-w-lg relative text-center">
                    <button onclick="document.getElementById('modal-registro').classList.add('hidden')" class="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                    <svg class="w-16 h-16 text-yellow-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    <h4 class="text-2xl text-white font-bold mb-2">Já Registrado</h4>
                    <p class="text-gray-400 mb-6">Você já possui este filme na sua lista pessoal.</p>
                    <button onclick="document.getElementById('modal-registro').classList.add('hidden')" class="w-full bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-4 rounded-lg transition-colors border border-gray-700">
                        Fechar Janela
                    </button>
                </div>""")
            
        novo_filme = ListaUsuario(
            usuario_id=usuario.id, 
            filme_id=existe_filme_db.id,
            status=status,         
            nota=nota,             
            comentario=comentario
        )
        session.add(novo_filme)
        session.commit()
               
        return HTMLResponse("""
            <div id="modal-content" class="bg-surface border border-gray-800 rounded-xl p-8 shadow-2xl w-full max-w-lg relative text-center">
                <button onclick="document.getElementById('modal-registro').classList.add('hidden')" class="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
                
                <svg class="w-16 h-16 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <h4 class="text-2xl text-white font-bold mb-2">Registro Salvo!</h4>
                <p class="text-gray-400 mb-6">O filme foi adicionado à sua lista com sucesso.</p>
                
                <button onclick="document.getElementById('modal-registro').classList.add('hidden')" class="w-full bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-4 rounded-lg transition-colors border border-gray-700">
                    Fechar Janela
                </button>
            </div>

            <button id="btn-adicionar" hx-swap-oob="true" class="mt-6 w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg shadow-lg transition-colors border border-green-500 cursor-default">
                ✓ Adicionado na Lista
            </button>""")

@app.put("/minhaLista/editar/{tmdb_id}")
def editarLista(request: Request, tmdb_id: int, status: str = Form(...), nota: Optional[int] = Form(None), 
                comentario: Optional[str] = Form(None), usuario_id: Optional[str] = Cookie(default=None)):
    
    if not usuario_id:
        response = HTMLResponse("")
        response.headers["HX-Redirect"] = "/login"
        return response
        
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        filme_db = session.exec(select(Filme).where(Filme.tmdb_id == tmdb_id)).first()
        
        if usuario and filme_db:
            relacao_usuario_filme = session.exec(select(ListaUsuario).where(
                ListaUsuario.usuario_id == usuario.id, 
                ListaUsuario.filme_id == filme_db.id
            )).first()
            
            if relacao_usuario_filme:

                relacao_usuario_filme.status = status
                relacao_usuario_filme.nota = nota
                relacao_usuario_filme.comentario = comentario

                session.add(relacao_usuario_filme)
                session.commit()
                
                return HTMLResponse("""
                    <div id="modal-content-edit" class="bg-surface border border-gray-800 rounded-xl p-8 shadow-2xl w-full max-w-lg relative text-center">
                        <svg class="w-16 h-16 text-blue-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <h4 class="text-2xl text-white font-bold mb-2">Alterações Salvas!</h4>
                        <p class="text-gray-400 mb-6">A sua avaliação foi atualizada.</p>
                        <button onclick="window.location.reload()" class="w-full bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-4 rounded-lg transition-colors border border-gray-700">
                            Fechar
                        </button>
                    </div>""")

@app.delete("/minhaLista/remover/{tmdb_id}")
def removerLista(request: Request, tmdb_id: int, usuario_id: Optional[str] = Cookie(default=None)):
    if not usuario_id:
        return Response(status_code=401)
        
    with Session(engine) as session:
        usuario = session.get(Usuario, int(usuario_id))
        filme_db = session.exec(select(Filme).where(Filme.tmdb_id == tmdb_id)).first()
        
        if usuario and filme_db:
            relacao_usuario_filme = session.exec(select(ListaUsuario).where(
                ListaUsuario.usuario_id == usuario.id, 
                ListaUsuario.filme_id == filme_db.id
            )).first()
            
            if relacao_usuario_filme:
                session.delete(relacao_usuario_filme)
                session.commit()
                
                response = HTMLResponse("")
                response.headers["HX-Refresh"] = "true"
                return response

"""
uvicorn main:app --reload

O Uvicorn é o "motor" que vai rodar o FastAPI.
O --reload faz com que o servidor atualize sozinho toda vez que você salvar o arquivo (ótimo para desenvolver).
"""