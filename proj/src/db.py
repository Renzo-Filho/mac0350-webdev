# app/database.py
from sqlmodel import SQLModel, create_engine, Session
from src.models import Usuario, Filme, ListaUsuario

# Cria o arquivo do banco localmente
sqlite_file_name = "hellomovie.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# O 'echo=True' faz o Python imprimir no terminal os comandos SQL que ele está gerando
engine = create_engine(sqlite_url, echo=True)

def criar_banco_e_tabelas():
    SQLModel.metadata.create_all(engine)

def obter_sessao():
    with Session(engine) as session:
        yield session