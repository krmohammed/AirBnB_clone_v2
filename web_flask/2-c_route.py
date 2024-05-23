#!/usr/bin/python3
""" starts a flask web app """
from flask import Flask


app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbtn():
    """ hello_hbtn route """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ hbnb route """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """ c route """
    text = text.replace("_", " ")
    return f"C {text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
