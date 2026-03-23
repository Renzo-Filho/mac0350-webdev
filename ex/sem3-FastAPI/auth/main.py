from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException, status, Cookie, Response
from typing import Annotated

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

db = [{"username": 'renzo', "password": '123'}]

@app.get('/', response_class=HTMLResponse)
async def returnHTML(request: Request):
    context = {"request": request, "message": ""}
    return templates.TemplateResponse("index.html", context)

@app.post('/users')
async def createAccount(request: Request, username: str = Form(...), password: str = Form(...)):
    for user in db:
            if user["username"] == username:
                context = {"request": request, "message": "Erro: Este nome de usuário já está em uso.", "login": False}
                return templates.TemplateResponse("index.html", context)
    
    new_user = {"username": username, "password": password}
    db.append(new_user)
    
    context = {"request": request, "message": "Conta criada com sucesso! Por favor, faça o login.", "login": True}
    return templates.TemplateResponse("index.html", context)

@app.get('/login', response_class=HTMLResponse)
async def returnLoginPage(request: Request):
    context = {"request": request, "message": "", "login": True}
    return templates.TemplateResponse("index.html", context)

@app.post('/login', response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    usuario_encontrado = None
    
    # Verifica se o usuário e a senha batem
    for u in db:
        if u["username"] == username and u["password"] == password:
            usuario_encontrado = u
            break
    
    # Se não encontrou, devolvemos a página de login com a mensagem de erro
    if not usuario_encontrado:
        context = {"request": request, "message": "Usuário ou senha inválidos", "login": True}
        return templates.TemplateResponse("index.html", context)
    
    # Se logou com sucesso, criamos o redirecionamento para a Home
    response = RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)

    # O servidor diz ao navegador para guardar o cookie 'session_user'
    response.set_cookie(key="session_user", value=username)
    
    return response

def get_active_user(session_user: Annotated[str | None, Cookie()] = None): # Lendo o Cookie
    # O FastAPI busca automaticamente um cookie chamado 'session_user'
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )
    
    user = next((u for u in db if u["username"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

@app.get('/home', response_class=HTMLResponse)
async def userHome(user: dict = Depends(get_active_user)):
    # Essa rota só executa se a dependência (get_active_user) não der erro.
    # O retorno de get_active_user é passado para a variável 'user'.
    
    html_content = f"""
    <html>
        <head><title>Home</title></head>
        <body>
            <h1>Bem-vindo à página protegida, {user['username']}!</h1>
            <p>Se você está vendo isso, é porque o cookie de sessão funcionou.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

"""
@app.get("/") retorna um template com o formulário de criação de usuário
@app.post("users") rota que vai criar usuários novos a partir do formulário
@app.get("login") retorna um template com o formulário de login
@app.post("login") recebe dados do formulário de login e retorna cookie de sessão
@app.get("home") rota protegida com o depends que depende do cookie de sessão
"""