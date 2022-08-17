"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Film
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

    # Todos los personajes #
@app.route('/people', methods=['GET'])
def people():

    characters = db.session.query(Character).all()
    if characters:
        return jsonify({
            "Characters": list(map(lambda character: character.serialize(), characters))
        })
    else:
        return jsonify({
            "Error": "No hay personajes aún"
        }), 404

    # Personaje especifico por id #
@app.route('/people/<int:id>')
def character(id):
    character = db.session.query(Character).get(id)
    if character:
        return jsonify({
            "Character": character.serialize()
        })
    else:
        return jsonify({
            "Error" : f"No existe el personaje con id={id}"
        }), 404

    # Todos los planetas #
@app.route('/planets', methods=['GET'])
def planets():
    planets = db.session.query(Planet).all()
    if planets:
        return jsonify({
            "Planets": list(map(lambda planet: planet.serialize(), planets))
        })
    else:
        return jsonify({
            "Error":"No hay planetas aun"
        })

    # Planeta especifico por id #
@app.route('/planets/<int:id>')
def planet(id):
    planet = db.session.query(Planet).get(id)
    if planet:
        return jsonify({
            "Planet": planet.serialize()
        })
    else:
        return jsonify({
            "Error": f"No existe el planeta con id={id}"
        })

    # Todos los vehiculos #
@app.route('/vehicles', methods=['GET'])
def vehicles():
    vehicles = db.session.query(Vehicle).all()
    if vehicles:
        return jsonify({
            "Vehicles": list(map(lambda vehicle: vehicle.serialize(), vehicles))
        })
    else:
        return jsonify({
            "Error":"No hay vehiculos aun"
        })

    # Planeta especifico por id #
@app.route('/vehicles/<int:id>')
def vehicle(id):
    vehicle = db.session.query(Vehicle).get(id)
    if vehicle:
        return jsonify({
            "Vehicle": vehicle.serialize()
        })
    else:
        return jsonify({
            "Error": f"No existe el vehiculo con id={id}"
        })

    # Todos los usuarios #
@app.route('/users')
def users():
    users = db.session.query(User).all()
    if users:
        return jsonify({
            "Users" : list(map(lambda user: user.serialize(), users))
        })
    else:
        return jsonify({
            "Error": "No hay usuarios aun"
        })

    # Favoritos del usuario conectado #
@app.route('/users/favorites', methods=['GET'])
def favs():
    # A modo de prueba se usa user_id = 1
    user_id = session["user_id"] if "user_id" in session else 1
    if user_id:
        user = db.session.query(User).get(user_id)
        return jsonify({
            "User" : user.serialize()
        })
    else:
        return jsonify({
            "Error": f"No existe el usuario"
        })

         # POST API ENDPOINT #
    # Añadir planeta a favoritos #
@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def add_planet_to_favs(planet_id):
    user_id = session["user_id"] if "user_id" in session else 1
    if user_id:
        user = db.session.query(User).get(user_id)
        planet = db.session.query(Planet).get(planet_id)
        if request.method == 'POST':
            user.favs_planets_id.append(planet)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se agrego planeta con exito"
            })
        elif request.method == 'DELETE':
            user.favs_planets_id.remove(planet)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se elimino el planeta de favoritos"
            })
        else:
            return jsonify({
                "Error": "Metodo no valido"
            }), 400
    else:
        return jsonify({
            "Error": "No se encuentra el usuario"
        })
    # Añadir personaje favorito #
@app.route('/favorite/people/<int:character_id>', methods=['POST', 'DELETE'])
def add_character_to_favs(character_id):
    user_id = session["user_id"] if "user_id" in session else 1
    if user_id:
        user = db.session.query(User).get(user_id)
        character = db.session.query(Character).get(character_id)
        if request.method == 'POST':
            user.favs_characters_id.append(character)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se agrego personaje con exito"
            })
        elif request.method == 'DELETE':
            user.favs_characters_id.remove(character)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se elimino personaje de favortios"
            })
        else:
            return jsonify({
                "Error": "Metodo no valido"
            }), 400
    else:
        return jsonify({
            "Error": "No se encuentra el usuario"
        })
    # Añadir vehiculo favorito #
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST', 'DELETE'])
def add_vehicle(vehicle_id):
    user_id = session["user_id"] if "user_id" in session else 1
    if user_id:
        user = db.session.query(User).get(user_id)
        vehicle = db.session.query(Vehicle).get(vehicle_id)
        if request.method == 'POST':
            user.favs_vehicles_id.append(vehicle)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se agrego vehiculo con exito"
            })
        elif request.method == 'DELETE':
            user.favs_vehicles_id.remove(vehicle)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "Message": "Se removio el vehiculo de favoritos"
            })
        else:
            return jsonify({
                "Error": "Metodo no valido"
            }), 400
    else:
        return jsonify({
            "Error": "No se encuentra el usuario"
        })

    # EndPoint para agregar data de personajes #
@app.route('/people/add', methods=['POST'])
def add_character():
    if request.method == 'POST':
        body = request.get_json()
        newCharacter = Character()
        newCharacter.name = body["name"]
        newCharacter.hair_color = body["hair_color"] if "hair_color" in body else "Unknow"
        newCharacter.birth_year = body["birth_year"]  if "birth_year" in body else "Unknow"
        newCharacter.url = body["url"]
        homeworldError = False
        vehicleError = False
        if "homeworld" in body:
            try:
                planet = db.session.query(Planet).get(body["homeworld"])
                newCharacter.homeworld.append(planet)
            except:
                homeworldError = True
                pass
        if "vehicles" in body:
            try:
                vehicle = db.session.query(Vehicle).get(body["vehicles"])
                newCharacter.vehicles.append(vehicle)
            except:
                vehicleError = True
                pass        
        db.session.add(newCharacter)
        db.session.commit()
        return jsonify({
            "Response" : "Se agrego personaje con exito",
            "Homeworld": "No se pudo agregar homeworld" if homeworldError else None,
            "Vehicle": "No se pudo agregar vehicle" if vehicleError else None,

        })
    else:
        return jsonify({
            "Error": "Metodo invalido"
        }), 400
    # Eliminar personaje #
@app.route('/people/add/<int:character_id>', methods=['PUT','DELETE'])
def put_or_del_character(character_id):
    character = db.session.query(Character).get(character_id)
    if request.method == 'PUT':
        body = request.get_json()
        for key in body:
            character[key] = body[key]
        db.session.add(character)
        db.session.commit()
        return jsonify({
            "Response" : "Se modifico personaje con exito",
        })
    elif request.method == 'DELETE':
        db.session.remove(character)
        db.session.commit()
        return jsonify({
            "Response" : "Se elimino personaje con exito",
        })
    else:
        return jsonify({
            "Error" : "Metodo invalido",
        }), 400

    # Añadir planeta #
@app.route('/planet/add', methods=['POST'])
def add_planet():
    if request.method == 'POST':
        body = request.get_json()
        newCharacter = Character()
        newCharacter.name = body["name"]
        newCharacter.hair_color = body["hair_color"] if "hair_color" in body else "Unknow"
        newCharacter.birth_year = body["birth_year"]  if "birth_year" in body else "Unknow"
        newCharacter.url = body["url"]
        if "homeworld" in body:
            try:
                planet = db.session.query(Planet).get(body["homeworld"])
                newCharacter.homeworld.append(planet)
            except:
                homeworldError = True
                pass
        if "vehicles" in body:
            try:
                vehicle = db.session.query(Vehicle).get(body["vehicles"])
                newCharacter.vehicles.append(vehicle)
            except:
                vehicleError = True
                pass        
        db.session.add(newCharacter)
        db.session.commit()
        return jsonify({
            "Response" : "Se agrego personaje con exito",
            "Homeworld": "No se pudo agregar homeworld" if homeworldError else None,
            "Vehicle": "No se pudo agregar vehicle" if vehicleError else None,

        })
    else:
        return jsonify({
            "Error": "Metodo invalido"
        }), 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
