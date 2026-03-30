from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)

class Filme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tmdb_id: int = Field(unique=True, index=True) # ID oficial do TMDb
    titulo: str
    sinopse: Optional[str] = None
    poster_url: Optional[str] = None
    data_lancamento: Optional[str] = None

class ListaUsuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    filme_id: int = Field(foreign_key="filme.id")
    status: str = Field(default="Planejado")
    nota: Optional[int] = Field(default=None, ge=0, le=10) # ge=0 (maior ou igual a 0), le=10 (menor ou igual a 10)