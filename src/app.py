"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    usersData = list(map(lambda user: user.serialize(), users))

    return jsonify(usersData), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_specific_user(id):
    oneUser = User.query.get(id)

    return jsonify(oneUser.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    charactersData = list(map(lambda character: character.serialize(), characters))

    return jsonify(charactersData), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_specific_character(id):
    oneCharacter = Character.query.get(id)

    return jsonify(oneCharacter.serialize()), 200

@app.route('/characters', methods=['POST'])
def add_character():
    chrInfo = request.get_json()
    character = Character()
    character.name = chrInfo['name']
    character.mass = chrInfo['mass']
    character.height = chrInfo['height']
    character.gender = chrInfo['gender']
    character.birth_year = chrInfo['birth_year']
    character.eye_color = chrInfo['eye_color']
    character.skin_color = chrInfo['skin_color']
    character.hair_color = chrInfo['hair_color']

    character.save()

    return jsonify(character.serialize()), 201

@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)
    character.delete()

    return jsonify({ "msg": "The character has been defeated"}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planetsData = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planetsData), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_specific_planet(id):
    onePlanet = Planet.query.get(id)

    return jsonify(onePlanet.serialize()), 200


@app.route('/planets', methods=['POST'])
def add_planet():
    pltInfo = request.get_json()
    planet = Planet()
    planet.name = pltInfo['name']
    planet.population = pltInfo['population']
    planet.gravity = pltInfo['gravity']
    planet.diameter = pltInfo['diameter']
    planet.climate = pltInfo['climate']
    planet.terrain = pltInfo['terrain']
    planet.surface_water = pltInfo['surface_water']
    planet.rotation_period = pltInfo['rotation_period']
    planet.orbital_period = pltInfo['orbital_period']

    planet.save()

    return jsonify(planet.serialize()), 201

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)
    planet.delete()

    return jsonify({ "msg": "The planet has been destroyed"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)