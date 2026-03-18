from flask import Flask
from generate_movie_db.bacon_distance import compute_bacon_distance
from generate_movie_db.exceptions import ActorNotFound
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/<actor_name>", methods=['GET'])
def bacon_distance(actor_name):
    try:
        print(actor_name)
        distance = compute_bacon_distance(actor_name)
    except ActorNotFound as e:
        return str(e)
    return str(distance)


@app.route("/", methods=['GET'])
def hi():
    return "invalid, please enter an actor name"
