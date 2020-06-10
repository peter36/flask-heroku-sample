# app.py
import os
import sys
from flask import Flask, request, jsonify
import psycopg2 as pg

DATABASE_URL = os.environ['DATABASE_URL']


def create_app():
    myapp = Flask(__name__)
    with myapp.app_context():
        init_db()
    return myapp

def get_connection():
    conn = pg.connect(DATABASE_URL, sslmode='require')
    return conn

def init_db():
    cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
    )
    conn = get_connection()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS cars")
        cur.execute("""
        CREATE TABLE cars(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price INT)
        """)
        query = "INSERT INTO cars (id, name, price) VALUES (%s, %s, %s)"
        cur.executemany(query, cars)
        con.commit()

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

# create app
app = create_app()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
