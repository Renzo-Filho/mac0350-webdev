
from typing import List
from sqlmodel import Field, Relationship, SQLModel
# Este import será importante em algum lugar...
# Dica: Olhe as outras dicas : D

class Aluno(SQLModel, table=True):
    nusp: int | None = Field(default=None, primary_key=True)
    nome: str
    idade: int

    # One to Many
    tarefas: List["Tarefa"] = Relationship(back_populates="aluno")     

class Tarefa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    duracao: int
    aluno_nusp: int = Field(foreign_key="aluno.nusp")

    aluno: Aluno = Relationship(back_populates="tarefas")


"""
Estruture os modelos e o relacionamento no banco de dados

Você deverá modelar apenas 1 tabela, com os seguintes parâmetros:

    Tabela de alunos:
        nome
        idade
        Acesso direto as tarefas - Veja as Dicas para descobrir como fazer isso

Para facilitar, a propriedade do ID já foi implementada em uma tabela, e na outra, a tarefa já está totalmente 
implementada, segue um template do código que você deverá completar:
"""