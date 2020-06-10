import os
import sys
import psycopg2 as pg

DATABASE_URL = os.environ['DATABASE_URL']

# get connection
def get_connection():
    conn = pg.connect(DATABASE_URL, sslmode='require')
    return conn


# init db
def init_db():
    cars = [
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
    ]
    conn = get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS cars")
        cur.execute("""
        CREATE TABLE cars(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price INT)
        """)
        query = "INSERT INTO cars (id, name, price) VALUES (%s, %s, %s)"
        cur.executemany(query, cars)
        conn.commit()


def get_all_cars():
  conn = get_connection()
  with conn:
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM cars")
    rows = cur.fetchall()
  return rows
