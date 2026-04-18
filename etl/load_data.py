import csv
import os
import psycopg2
from psycopg2.extras import execute_values

DATA_LAKE_DIR = '/downloads'
DB_PARAMS = {
    'host': os.getenv('PGHOST', 'db'),
    'port': os.getenv('PGPORT', '5432'),
    'dbname': os.getenv('PGDATABASE', 'movieflix_dw'),
    'user': os.getenv('PGUSER', 'movieflix'),
    'password': os.getenv('PGPASSWORD', 'movieflix'),
}

CSV_FILES = {
    'movies': 'movies.csv',
    'users': 'users.csv',
    'ratings': 'ratings.csv',
}

SQL_INSERTS = {
    'movies': 'INSERT INTO movies (movie_id, title, year, genre, director) VALUES %s ON CONFLICT (movie_id) DO NOTHING',
    'users': 'INSERT INTO users (user_id, name, email, country, age) VALUES %s ON CONFLICT (user_id) DO NOTHING',
    'ratings': 'INSERT INTO ratings (user_id, movie_id, score, rating_date) VALUES %s',
}

FIELDNAMES = {
    'movies': ['movie_id', 'title', 'year', 'genre', 'director'],
    'users': ['user_id', 'name', 'email'],
    'ratings': ['user_id', 'movie_id', 'rating', 'timestamp'],
}

CASTS = {
    'movies': {'year': lambda x: int(x) if x else None},
    'users': {'user_id': int},
    'ratings': {'user_id': int, 'rating': int},
}


def synthetic_user_profile(user_id):
    countries = ['Brazil', 'USA', 'Canada', 'India', 'Mexico', 'UK']
    age_groups = [18, 23, 30, 42, 56]
    index = user_id % len(countries)
    age_index = user_id % len(age_groups)
    return countries[index], age_groups[age_index]


def load_csv_to_db(table_name):
    path = os.path.join(DATA_LAKE_DIR, CSV_FILES[table_name])
    rows = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            if table_name == 'movies':
                values = [
                    row.get('movie_id', '').strip(),
                    row.get('title', '').strip(),
                    CASTS['movies']['year'](row.get('year', '').strip()) if row.get('year', '').strip() else None,
                    row.get('genre', '').strip(),
                    row.get('director', '').strip(),
                ]
            elif table_name == 'users':
                user_id = int(row.get('user_id', '').strip())
                country, age = synthetic_user_profile(user_id)
                values = [
                    user_id,
                    row.get('name', '').strip(),
                    row.get('email', '').strip(),
                    country,
                    age,
                ]
            else:
                raw_date = row.get('timestamp', '').strip()
                rating_date = raw_date or None
                values = [
                    int(row.get('user_id', '').strip()),
                    row.get('movie_id', '').strip(),
                    int(row.get('rating', '').strip()),
                    rating_date,
                ]
            rows.append(tuple(values))

    if not rows:
        print(f'No rows found for {table_name}')
        return

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            execute_values(cur, SQL_INSERTS[table_name], rows)
            conn.commit()
            print(f'Loaded {len(rows)} rows into {table_name}')


def main():
    for table in ['movies', 'users', 'ratings']:
        load_csv_to_db(table)


if __name__ == '__main__':
    main()
