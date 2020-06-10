# app.py
import os
import sys
from flask import Flask, request, jsonify
import psycopg2 as pg
from repo import *

def create_app():
    myapp = Flask(__name__)
    with myapp.app_context():
        init_db()
    return myapp

# create app
app = create_app()

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


@app.route('/getcars/', methods=['GET'])
def getcars():
    response = {}
    try:
        results = get_all_cars()
        response["MESSAGE"] = results
    except Exception as error:
        print(error)
        response["ERROR"] = "Server error"

    # Return the response in json format
    return jsonify(response)


@app.route('/addcar/', methods=['POST'])
def getcars():
    name = request.form.get('name')
    price = request.form.get('price')
    response = {}
    try:
        results = add_one_car(name, price)
        response["MESSAGE"] = results
    except Exception as error:
        print(error)
        response["ERROR"] = "Server error"

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

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
