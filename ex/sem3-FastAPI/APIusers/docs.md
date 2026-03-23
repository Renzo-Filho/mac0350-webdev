## 📘 Guia Fundamental: FastAPI

### 1. O que é e Por que usar?
O **FastAPI** é um framework web moderno para Python 3.8+ focado em performance e produtividade.

* **Velocidade Máxima:** Graças ao `Starlette` e `Pydantic`, ele é um dos frameworks Python mais rápidos (nível Go/Node.js).
* **Documentação Automática:** Ao criar uma rota, ele gera o `/docs` (Swagger UI) instantaneamente.
* **Segurança de Tipos:** Ele usa *Type Hints* do Python para validar se o que chegou é o que você esperava (ex: converter texto da web em `int`).

---

### 2. Anatomia de uma Requisição (Request)
Quando o navegador (ou o HTMX) fala com o seu servidor, ele envia informações de diferentes formas. É crucial saber onde colocar cada dado.


| Local do Dado | Exemplo na URL/Requisição | Uso no FastAPI |
| :--- | :--- | :--- |
| **Path Parameter** | `/users/10` | Identificar um recurso específico (ID). |
| **Query Parameter** | `/users?status=ativo` | Filtrar, ordenar ou buscar dados. |
| **Request Body** | *Invisível na URL* (JSON ou Form) | Enviar objetos complexos (Cadastros, Logins). |

---

### 3. Extraindo Dados no Código
Aqui está o guia de "tradução" entre o que o usuário envia e como você recebe no Python:

#### **A. Parâmetros Simples (Path e Query)**
```python
@app.get("/items/{item_id}") # item_id está na rota (Path)
async def read_item(item_id: int, q: str = None): # `q` não está na rota (Query)
    return {"id": item_id, "busca": q}
```

#### **B. Formulários (HTMX/HTML)**
Como o HTMX envia dados como "formulário", usamos a classe `Form`. O `...` (Ellipsis) indica que o campo é **obrigatório**.
```python
from fastapi import Form

@app.post("/users")
async def create_user(nome: str = Form(...), idade: int = Form(...)):
    return {"status": "criado", "nome": nome}
```

#### **C. Modelos Complexos (Pydantic)**
Ideal para JSON e APIs de larga escala. O `Field` permite adicionar regras de validação.
```python
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(..., min_length=3) # Obrigatório e min 3 caracteres
    idade: int = Field(default=18, ge=0)      # Padrão 18, maior ou igual a 0
```
---

### 4. O Ciclo de Vida (Como o dado viaja)

1.  **O Usuário** clica no botão do formulário HTMX.
2.  **O Navegador** envia os dados no **Body** (corpo) da requisição.
3.  **O FastAPI** intercepta, verifica o tipo (`str`, `int`), valida se não está vazio (`...`) e converte.
4.  **A Função** recebe os dados prontos para serem salvos no banco.
5.  **A Resposta** (HTML ou JSON) é enviada de volta para a tela.

---
---
---

## 📚 Documentação: API de Usuários (Versão JSON)

### 1. A Estratégia: Por que Pydantic?
Como o HTML utiliza a extensão `json-enc`, o navegador não envia os dados como um formulário comum, mas sim como um objeto JSON. 
* **A Mudança:** Substituímos o `Form(...)` por um modelo **Pydantic**.
* **O Ganho:** O Pydantic valida a estrutura do JSON automaticamente. Se o JSON chegar incompleto, o FastAPI bloqueia a requisição antes mesmo de ela chegar na sua função.



---

### 2. Definição dos Endpoints

| Método | Rota | Descrição | Entrada |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Entrega a interface visual (HTML). | Nenhuma |
| **POST** | `/users` | Adiciona um novo usuário à lista global. | **JSON Body** (Nome e Idade) |
| **GET** | `/users` | Lista todos os usuários ou um específico. | **Query Param** (`index`) |
| **DELETE** | `/users` | Reseta (esvazia) o banco de dados temporário. | Nenhuma |

---

### 3. Detalhes da Implementação

#### **A. O Modelo de Dados**
Para ler o JSON enviado pelo HTMX, definimos a estrutura esperada:
```python
class User(BaseModel):
    nome: str
    idade: int
```

#### **B. O Parâmetro de Consulta (Query Parameter)**
Diferente do Path Parameter (que faz parte da URL fixa), o **Query Parameter** é opcional e vem após o `?`. No seu código, ele permite a busca dinâmica:
* Se você enviar `index=0`, a API retorna apenas o primeiro usuário.
* Se não enviar nada, a API entende que `index` é `None` e retorna a lista completa.
