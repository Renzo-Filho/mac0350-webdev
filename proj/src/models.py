from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome_usuario: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    senha: str

class Filme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tmdb_id: int = Field(unique=True, index=True) 
    titulo: str
    sinopse: Optional[str] = None
    poster_url: Optional[str] = None
    data_lancamento: Optional[str] = None

class ListaUsuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    filme_id: int = Field(foreign_key="filme.id")
    status: str = Field(default="Quero ver") 
    nota: Optional[int] = Field(default=None, ge=0, le=10)
    comentario: Optional[str] = None