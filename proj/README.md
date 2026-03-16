# Projeto: HelloMovie – Gerenciador Pessoal de Filmes e Séries

## 1. Descrição do Projeto

O **HelloMovie** é uma aplicação web fullstack destinada a entusiastas de cinema que desejam organizar suas experiências assistindo filmes e séries. Inspirado em plataformas como MyAnimeList e Letterboxd, o sistema permitirá que usuários busquem títulos em uma base de dados global, adicionem-nos a listas personalizadas, avaliem sua experiência e gerenciem seu progresso.
O projeto será desenvolvido como parte da disciplina de *Introdução ao Desenvolvimento de Sistemas de Software*.

## 2. Objetivos Principais (MVP)

* **Busca de Títulos:** Integração com API externa para consulta de metadados de filmes/séries (título, sinopse, capa, nota média).
* **Gerenciamento de Lista (CRUD):** Permitir que o usuário adicione títulos à sua lista pessoal, edite o status (Planejado, Assistindo, Finalizado) e remova itens.
* **Persistência de Dados:** Garantir que a lista do usuário seja salva em um banco de dados e recuperada em acessos futuros.

## 3. Arquitetura

Para garantir a experiência fullstack, a aplicação será dividida em três camadas:

* **Frontend:** Interface web responsiva para interação com o usuário.

* **Backend:** Servidor responsável pelas regras de negócio e intermediação com o banco de dados.

* **Banco de Dados:** Armazenamento das listas dos usuários.

* **API Externa:** Consumo de dados via **TMDb (The Movie Database)**.

## 4. Algumas Funcionalidades Planejadas

1. **Pesquisa:** Barra de busca que consome a API do TMDb e exibe resultados em tempo real.
2. **Minha Lista:** Uma área restrita onde o usuário visualiza seus filmes salvos.
3. **Sistema de Status:** Possibilidade de marcar filmes como "Já vi", "Quero ver" ou "Favorito".
4. **Avaliação:** Atribuição de uma nota pessoal (1 a 10) para cada título na lista do usuário.

---
