-- Informações dos Usuários da aplicação
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Catálogo (Cache local dos filmes buscados na API do TMDb)
CREATE TABLE filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER UNIQUE NOT NULL, -- ID original da API externa
    titulo VARCHAR(200) NOT NULL,
    sinopse TEXT,
    poster_url VARCHAR(255),
    data_lancamento DATE
);

-- A Lista Pessoal (Tabela relacional entre Usuário e Filme)
CREATE TABLE lista_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    filme_id INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'Planejado', -- Ex: Planejado, Assistindo, Finalizado
    nota INTEGER CHECK (nota >= 0 AND nota <= 10), -- Avaliação pessoal de 0 a 10
    data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Chaves Estrangeiras 
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    FOREIGN KEY (filme_id) REFERENCES filmes (id) ON DELETE CASCADE,
    
    -- Garante que um usuário não adicione o mesmo filme duas vezes na sua lista
    UNIQUE(usuario_id, filme_id)
);