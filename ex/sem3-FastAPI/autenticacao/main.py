from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Optional

app = FastAPI()

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Banco de dados simulado (use um banco real em produção)
users_db = {}

@app.get("/")
async def auth_page(request: Request, message: Optional[str] = None):
    """Página de autenticação"""
    context = {
        "request": request,
        "message": {"type": "success", "text": message} if message else None
    }
    return templates.TemplateResponse("auth.html", context)

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False)
):
    """Processa o login"""
    # Aqui você verificará as credenciais no banco de dados
    if email in users_db and users_db[email]["password"] == password:
        # Login bem-sucedido - redirecionar para dashboard
        response = RedirectResponse(url="/dashboard", status_code=303)
        if remember:
            # Configurar cookie de longa duração
            response.set_cookie(key="session", value=email, max_age=30*24*3600)
        else:
            response.set_cookie(key="session", value=email)
        return response
    else:
        # Login falhou
        context = {
            "request": request,
            "message": {"type": "error", "text": "E-mail ou senha inválidos"}
        }
        return templates.TemplateResponse("auth.html", context, status_code=401)

@app.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    terms: bool = Form(False)
):
    """Processa o cadastro"""
    # Validações
    if password != confirm_password:
        context = {
            "request": request,
            "message": {"type": "error", "text": "As senhas não coincidem"}
        }
        return templates.TemplateResponse("auth.html", context, status_code=400)
    
    if len(password) < 6:
        context = {
            "request": request,
            "message": {"type": "error", "text": "A senha deve ter pelo menos 6 caracteres"}
        }
        return templates.TemplateResponse("auth.html", context, status_code=400)
    
    if not terms:
        context = {
            "request": request,
            "message": {"type": "error", "text": "Você deve aceitar os termos de uso"}
        }
        return templates.TemplateResponse("auth.html", context, status_code=400)
    
    if email in users_db:
        context = {
            "request": request,
            "message": {"type": "error", "text": "Este e-mail já está cadastrado"}
        }
        return templates.TemplateResponse("auth.html", context, status_code=400)
    
    # Salvar usuário (em produção, hash a senha!)
    users_db[email] = {
        "name": name,
        "password": password,  # NUNCA faça isso! Use hash!
        "email": email
    }
    
    # Redirecionar para login com mensagem de sucesso
    return RedirectResponse(
        url="/?message=Cadastro realizado com sucesso! Faça login.",
        status_code=303
    )

@app.get("/dashboard")
async def dashboard(request: Request):
    """Página protegida (exige login)"""
    # Verificar se usuário está logado
    session = request.cookies.get("session")
    if not session or session not in users_db:
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user": users_db[session]}
    )

@app.get("/logout")
async def logout():
    """Fazer logout"""
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response