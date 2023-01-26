"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
import json
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Character_X_Vehicle, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/character/create', methods=['POST'])
def create_character():
    luke_dict = {
    "name": "Luke Skywalker",
    "url": "https://swapi.dev/api/people/1/",
    "height_in_cm": 172,
    "mass_in_kg": 77,
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birthyear": "19BBY",
    "gender": "male",
    "planet_id": 1
    }
    leia_dict = {
        "name": "Leia Organa",
        "url": "https://swapi.dev/api/people/5/",
        "height_in_cm": 150,
        "mass_in_kg": 49,
        "hair_color": "brown",
        "skin_color": "light",
        "eye_color": "brown",
        "birthyear": "19BBY",
        "gender": "female",
        "planet_id": 2
    }
    characters_list = [luke_dict, leia_dict]
    characters = [Character(**char) for char in characters_list]
    db.session.add_all(characters)
    db.session.commit()



@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify(characters)

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
