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

# Characters
# ------------------------------------------------------------

@app.route('/characters/create', methods=['POST'])
def create_character():
    # luke_dict = {
    # "name": "Luke Skywalker",
    # "url": "https://swapi.dev/api/people/1/",
    # "height_in_cm": 172,
    # "mass_in_kg": 77,
    # "hair_color": "blond",
    # "skin_color": "fair",
    # "eye_color": "blue",
    # "birthyear": "19BBY",
    # "gender": "male",
    # "planet_id": None
    # }
    # leia_dict = {
    #     "name": "Leia Organa",
    #     "url": "https://swapi.dev/api/people/5/",
    #     "height_in_cm": 150,
    #     "mass_in_kg": 49,
    #     "hair_color": "brown",
    #     "skin_color": "light",
    #     "eye_color": "brown",
    #     "birthyear": "19BBY",
    #     "gender": "female",
    #     "planet_id": None
    # }
    # characters_list = [luke_dict, leia_dict]
    # characters = [Character(**char) for char in characters_list]
    # db.session.add_all(characters)
    # db.session.commit()
    return {"msg": "create character"}

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = []
    for character in Character.query.all():
        characters.append(character.serialize())
    return jsonify(characters)

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    # print(Character.query.all())
    print(character)
    return jsonify(character.serialize())

@app.route('/characters/<int:character_id>/vehicles', methods=['GET'])
def get_character_vehicles(character_id):
    character = Character.query.get(character_id)
    vehicles = character.vehicles
    return jsonify(vehicles)

# Planets
# --------------------------------------------------------

@app.route('/planets/create', methods=['POST'])
def create_planet():
    # tatooine_dict = {
    #     "name": "Tatooine",
    #     "url": "https://swapi.dev/api/planets/1/",
    #     "diameter_in_km": 10465,
    #     "rotation_period_in_days": 23,
    #     "orbital_period_in_days": 304,
    #     "gravity_in_g": 1,
    #     "population": 200000,
    #     "climate": "arid",
    #     "terrain": "desert",
    #     "surface_water_percent": 1
    # }
    # alderan_dict = {
    #     "name": "Alderaan",
    #     "url": "https://swapi.dev/api/planets/2/",
    #     "diameter_in_km": 12500,
    #     "rotation_period_in_days": 24,
    #     "orbital_period_in_days": 364,
    #     "gravity_in_g": 1,
    #     "population": 2000000000,
    #     "climate": "temperate",
    #     "terrain": "grasslands, mountains",
    #     "surface_water_percent": 40
    # }
    # planets_list = [tatooine_dict, alderan_dict]
    # planets = [Planet(**planet) for planet in planets_list]
    # db.session.add_all(planets)
    # db.session.commit()
    return {"msg": "create planet"}

@app.route('/planets', methods=['GET'])
def get_planets():
        planets = []
        for planet in Planet.query.all():
            planets.append(planet.serialize())
        return jsonify(planets)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
        planet = Planet.query.filter_by(id=planet_id).first()
        # print(Character.query.all())
        print(planet)
        return jsonify(planet.serialize())

# Vehicles
# ------------------------------------------------------

@app.route('/vehicles/create', methods=['POST'])
def crete_vehicle():
    speeder_bike_dict = {
        "name": "Speeder Bike",
        "url": "https://swapi.co/api/vehicles/1/",
        "model": "74-Z",
        "vehicle_class": "Speeder",
        "manufacturer": "Aratech Repulsor Company",
        "cost_in_credits": "8000",
        "length_in_m": "3.2",
        "crew": "1",
        "passengers": "1",
        "max_atmosphering_speed_in_kmh": "360",
        "cargo_capacity_in_kg": "4"
    }
    millennium_falcon_dict = {
        "name": "Millennium Falcon",
        "url": "https://swapi.co/api/vehicles/10/",
        "model": "YT-1300 light freighter",
        "vehicle_class": "light freighter",
        "manufacturer": "Corellian Engineering Corporation",
        "cost_in_credits": "100000",
        "length_in_m": "34.37",
        "crew": "4",
        "passengers": "6",
        "max_atmosphering_speed_in_kmh": "1050",
        "cargo_capacity_in_kg": "100000"
    }
    vehicles_list = [speeder_bike_dict, millennium_falcon_dict]
    vehicles = [Vehicle(**vehicle) for vehicle in vehicles_list]
    db.session.add_all(vehicles)
    db.session.commit()
    return {"msg": "create vehicle"}

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return {}

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    return {}

# Sitemap
# -------------------------------------------------------
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Launch
# ---------------------------------------------------------
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
