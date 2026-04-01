# 🎬 HelloMovie

<div align="center">
  <p><strong>Seu Diário Cinematográfico Pessoal</strong></p>
  <p>Uma aplicação web fullstack para buscar, registrar e gerenciar seus filmes favoritos, inspirada em plataformas como Letterboxd.</p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HTMX-336699?style=for-the-badge&logo=htmx&logoColor=white" alt="HTMX" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
</div>

<br>

> **Nota:** Este projeto foi desenvolvido como parte da disciplina de *Introdução ao Desenvolvimento de Sistemas de Software*.

## ✨ Funcionalidades

- **Autenticação Segura:** Criação de conta e login utilizando criptografia de senhas (Bcrypt) e controle de sessão via Cookies.
- **Integração com TMDb:** Busca de filmes em tempo real, resgate de pôsteres, sinopses, elenco e tendências atuais diretamente da API do The Movie Database.
- **Catálogo Pessoal (CRUD Completo via HTMX):**
  - **Adicionar:** Salve filmes na sua lista pessoal.
  - **Ler:** Visualize seus filmes salvos com filtros dinâmicos (Já vi, Quero ver, Assistindo, Favorito).
  - **Atualizar:** Edite o status, dê uma nota de 1 a 10 e escreva uma análise/review pessoal.
  - **Deletar:** Remova filmes da sua lista de forma interativa e segura.
- **Comunidade (Rede Social):** Compartilhe suas opiniões! A página de detalhes de cada filme exibe as avaliações, notas e comentários feitos por outros usuários da plataforma.
- **Interface Responsiva:** Design moderno feito com Tailwind CSS, totalmente adaptável para dispositivos móveis e desktops.
- **Single Page Application (SPA) Feel:** Graças ao HTMX, as interações de banco de dados e atualizações de UI (como o modal de registro) ocorrem de forma suave, sem necessidade de recarregar a página inteira a cada clique.

## 📸 Screenshots

<div align="center">
  <img src="src/assets/photo1.png" alt="Tela Inicial" width="48%">
  <img src="src/assets/photo4.png" alt="Detalhes do Filme" width="48%">
</div>
<div align="center">
  <img src="src/assets/photo2.png" alt="Minha Lista" width="48%">
  <img src="src/assets/photo3.png" alt="Perfil do Usuário" width="48%">
</div>

## 🛠️ Tecnologias Utilizadas

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web de alta performance.
- [SQLModel](https://sqlmodel.tiangolo.com/) - ORM para interação com o banco de dados SQLite.
- [Passlib & Bcrypt](https://passlib.readthedocs.io/) - Hashing de senhas.

**Frontend:**
- [Jinja2](https://jinja.palletsprojects.com/) - Motor de templates HTML.
- [HTMX](https://htmx.org/) - Interações AJAX direto no HTML (hx-get, hx-post, hx-put, hx-delete).
- [Tailwind CSS](https://tailwindcss.com/) - Estilização utilitária.

## 🚀 Como Rodar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10+ instalado em sua máquina. Você também precisará de uma chave de API (Read Access Token) do [TMDb](https://developer.themoviedb.org/docs/getting-started).

### 2. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/hellomovie.git]
cd hellomovie
```

### 3. Criar e Ativar o Ambiente Virtual
```bash
# No Windows:
python -m venv .venv
.venv\Scripts\activate

# No Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione o seu token do TMDb:
```env
TMDB_READ_TOKEN=seu_token_aqui_gigante_fornecido_pelo_tmdb
```

### 6. Iniciar o Servidor
Execute o comando abaixo para iniciar o Uvicorn:
```bash
uvicorn src.main:app --reload
```
A aplicação estará disponível em `http://127.0.0.1:8000`. 
*(O banco de dados SQLite será criado automaticamente no primeiro acesso).*
