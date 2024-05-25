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


@app.route("/states", strict_slashes=False)
def states():
    """ list of states """
    all_states = storage.all(State).values()
    return render_template("7-states_list.html", states=all_states)

@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """ states by id """
    states = storage.all(State).values()
    for state in states:
        if id == state.id:
            return render_template("9-states.html", state=state)
    return render_template("9-not_found.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
