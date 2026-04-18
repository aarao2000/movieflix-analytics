-- 5 filmes mais populares (por número de avaliações)
SELECT
  m.title,
  m.genre,
  COUNT(r.rating_id) AS total_ratings,
  AVG(r.score) AS avg_score
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.title, m.genre
ORDER BY total_ratings DESC
LIMIT 5;

-- Gênero com melhor avaliação média
SELECT
  genre,
  AVG(score) AS avg_score,
  COUNT(rating_id) AS total_ratings
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY genre
HAVING COUNT(rating_id) >= 5
ORDER BY avg_score DESC
LIMIT 1;

-- País com mais avaliações
SELECT
  country,
  COUNT(r.rating_id) AS total_ratings,
  AVG(r.score) AS avg_score
FROM ratings r
JOIN users u ON r.user_id = u.user_id
GROUP BY country
ORDER BY total_ratings DESC
LIMIT 5;

-- Top 10 filmes mais bem avaliados por gênero (Data Mart)
SELECT * FROM top_10_rated_by_genre;

-- Nota média por faixa etária dos usuários (Data Mart)
SELECT * FROM avg_score_by_age_group;

-- Número de avaliações por país (Data Mart)
SELECT * FROM ratings_by_country;
