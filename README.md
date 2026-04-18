# MovieFlix Analytics

MovieFlix Analytics é um projeto de exemplo que une uma aplicação web simples de cadastro e avaliação de filmes com um fluxo de dados analítico.

## Arquitetura

- `app/`: aplicação Flask para cadastro de filmes e notas.
- `nginx/`: configuração de proxy reverso Nginx.
- `postgres/`: esquema inicial do Data Warehouse e visões do Data Mart.
- `data_lake/`: arquivos CSV brutos usados como Data Lake.
- `etl/`: scripts de carga ETL que importam os CSVs para o PostgreSQL.
- `.github/workflows/`: pipeline de CI/CD para build, teste e push de imagem Docker.

## Como rodar localmente

1. Acesse o diretório do projeto:
   ```bash
   cd ~/movieflix-analytics
   ```

2. Suba os containers com Docker Compose:
   ```bash
   docker compose up --build
   ```

3. Abra a aplicação no navegador:
   - `http://localhost:8080`

4. Carregue os dados do Data Lake para o Data Warehouse:
   ```bash
   docker compose run --rm app python etl/load_data.py
   ```

5. Conecte-se ao PostgreSQL para consultar o Data Mart:
   - host: `localhost`
   - porta: `5432`
   - database: `movieflix_dw`
   - usuário: `movieflix`
   - senha: `movieflix`

## Dados e visões

- Data Lake: `data_lake/movies.csv`, `data_lake/users.csv`, `data_lake/ratings.csv`
- Data Warehouse: tabelas `movies`, `users`, `ratings` (o carregamento enriquece `users` com país e idade sintéticos para análise)
- Data Mart: views `top_10_rated_by_genre`, `avg_score_by_age_group`, `ratings_by_country`

## Consultas analíticas

A pasta `postgres/queries.sql` contém exemplos de queries importantes:
- Quais são os 5 filmes mais populares?
- Qual gênero tem a melhor avaliação média?
- Qual país gera mais avaliações?
- Consultas de Data Mart para visões resumidas.

## CI/CD

O workflow GitHub Actions `./github/workflows/docker-ci.yml`:
- builda a imagem Docker da aplicação
- testa se a aplicação responde na porta correta
- faz push para Docker Hub usando `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`

## Observações

- O Nginx atua como proxy reverso para o serviço Flask.
- A aplicação web usa SQLite local para armazenamento da interface e Postgres para o Data Warehouse.
