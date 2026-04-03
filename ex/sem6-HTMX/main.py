from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

curtidas = 0
aba_atual = "curtidas" 

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {
        "request": request, 
        "curtidas": curtidas,
        "aba_atual": aba_atual
    }

    return templates.TemplateResponse("index.html", context)

@app.post("/curtir")
async def curtir():
    global curtidas
    curtidas += 1

    return str(curtidas)

@app.post("/resetar-curtidas")
async def resetarCurtidas():
    global curtidas
    curtidas = 0

    return str(curtidas)

@app.post("/mudar-aba")
async def mudarAba(request: Request, aba: str = Form(...)):
    global aba_atual
    aba_atual = aba
    
    if aba == "curtidas":
        return templates.TemplateResponse("curtidas.html", {"request": request, "curtidas": curtidas})
    elif aba == "jupiter":
        return templates.TemplateResponse("jupiter.html", {"request": request})
    elif aba == "professor":
        return templates.TemplateResponse("professor.html", {"request": request})

@app.get("/proxima-aba")
async def proximaAba(request: Request): 
    global aba_atual
    
    abas = ["curtidas", "jupiter", "professor"]

    index_atual = abas.index(aba_atual)
    prox_index = (index_atual + 1) % len(abas)
    nova_aba = abas[prox_index]
    
    aba_atual = nova_aba
    
    if nova_aba == "curtidas":
        return templates.TemplateResponse("curtidas.html", {"request": request, "curtidas": curtidas})
    elif nova_aba == "jupiter":
        return templates.TemplateResponse("jupiter.html", {"request": request})
    elif nova_aba == "professor":
        return templates.TemplateResponse("professor.html", {"request": request})