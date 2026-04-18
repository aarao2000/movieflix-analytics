CREATE TABLE IF NOT EXISTS movies (
    movie_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    director TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    country TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    movie_id TEXT REFERENCES movies(movie_id),
    score INTEGER,
    rating_date DATE
);

CREATE OR REPLACE VIEW top_10_rated_by_genre AS
SELECT
    genre,
    title,
    AVG(r.score) AS avg_score,
    COUNT(r.rating_id) AS ratings_count
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY genre, title
HAVING COUNT(r.rating_id) >= 2
ORDER BY genre, avg_score DESC
LIMIT 10;

CREATE OR REPLACE VIEW avg_score_by_age_group AS
SELECT
    CASE
      WHEN age < 18 THEN '0-17'
      WHEN age BETWEEN 18 AND 24 THEN '18-24'
      WHEN age BETWEEN 25 AND 34 THEN '25-34'
      WHEN age BETWEEN 35 AND 49 THEN '35-49'
      ELSE '50+' END AS age_group,
    AVG(r.score) AS avg_score,
    COUNT(r.rating_id) AS ratings_count
FROM ratings r
JOIN users u ON r.user_id = u.user_id
GROUP BY age_group
ORDER BY avg_score DESC;

CREATE OR REPLACE VIEW ratings_by_country AS
SELECT
    u.country,
    COUNT(r.rating_id) AS total_ratings,
    AVG(r.score) AS avg_score
FROM ratings r
JOIN users u ON r.user_id = u.user_id
GROUP BY u.country
ORDER BY total_ratings DESC;
