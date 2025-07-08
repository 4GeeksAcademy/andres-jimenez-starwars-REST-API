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
from models import db, User, People, Planet, Favorite
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

#-------------------- PEOPLE ---------------------
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([{"id": people.id, "name": people.name, "height": people.height, "gender": people.gender} for people in people])

@app.route('/people/<int:people_id>', methods=["GET"])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify({"id": person.id, "name": person.name, "height": person.height, "gender": person.gender})
    return jsonify({"error": "Person not found"}), 404


#------------------- PLANETS ---------------------
@app.route('/planets', methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    if planets:
        return jsonify([{"id": planets.id, "name": planets.name, "terrain": planets.terrain, "population": planets.population} for planets in planets]), 200
    else:
        return jsonify({"msg": "No planets found"}), 404

@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({"id": planet.id, "name": planet.name, "terrain": planet.terrain, "population": planet.population})
    return jsonify({"error": "Planet not found"}), 404


#-------------------- USER --------------------------
@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": users.id, "email": users.email,} for users in users])

@app.route('/users/favorites', methods=["GET"])
def get_user_favorites():
    user_id = 1 #Hardcoaded for now.
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    response = []
    for favorite in favorites:
        if favorite.planet:
            response.append({"type": "planet", "name": favorite.planet.name})
        elif favorite.character:
            response.append({"type": "character", "name": favorite.character.name})
    
    return jsonify(response), 200


#--------------------- ADD FAVORITES --------------------
@app.route('/favorite/planet/<int:planet_id>', methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = 1
    favorite = Favorite(user_id = user_id, planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet added"}), 201

@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_people(people_id):
    user_id = 1
    favorite = Favorite(user_id = user_id, people_id = people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person added"}), 201



#-------------------- DELETE FAVORITES ---------------------
@app.route('/favorite/planet/<int:planet_id>', methods=["DELETE"])
def delete_favorire_planet(planet_id):
    user_id = 1
    favorite = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"})

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_favorire_people(people_id):
    user_id = 1
    favorite = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person deleted"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
