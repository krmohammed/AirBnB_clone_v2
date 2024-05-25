#!/usr/bin/python3
""" starts a flask web app """
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_database(exception):
    """ removes the current SQLAlchemy session """
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """ list of states and their cities """
    all_states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=all_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
