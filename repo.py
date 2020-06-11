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
    ('Audi', 52642),
    ('Mercedes', 57127),
    ('Skoda', 9000),
    ('Volvo', 29000),
    ('Bentley', 350000),
    ('Citroen', 21000),
    ('Hummer', 41400),
    ('Volkswagen', 21600)
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
        query = "INSERT INTO cars (name, price) VALUES (%s, %s)"
        cur.executemany(query, cars)
        conn.commit()


def get_all_cars():
  conn = get_connection()
  with conn:
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM cars")
    rows = cur.fetchall()
  return rows


def add_one_car(name, price):
  conn = get_connection()
  id = -1
  with conn:
    cur = conn.cursor()
    query = "INSERT INTO cars (name, price) VALUES (%s, %s) RETURNING id"
    id = cur.execute(query, (name, price))
  return id

