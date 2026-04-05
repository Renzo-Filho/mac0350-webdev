from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "hellomovie.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def criar_banco_de_dados():
    SQLModel.metadata.create_all(engine)

def obter_sessao():
    with Session(engine) as session:
        yield session