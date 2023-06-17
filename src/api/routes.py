"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Agencia, Viajero, PaqueteDeViaje
from api.utils import generate_sitemap, APIException
import hashlib

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    #verifys payload body
    if username == None or password == None:
        return jsonify({"msg": "Bad username or password ⛔️"}), 401
    #search user existance into the DB
    search_user = User.query.filter_by(username=username).one_or_none()
    if search_user == None:
            return jsonify({ "message" : "user not found "}), 404
    #verify thats the password is correct
    #password saved as hash // with the password arriving hashed
    # if search_user.password == hashlib.md5(password.encode('utf-8') ).hexdigest():
    #     return jsonify({ "token" : create_access_token(identity=search_user.email) }), 200

    agencia = None
    viajero = None

    if search_user.rol == 1:
        agencia = Agencia.query.filter_by(user_id = search_user.id).one_or_none()
    else:
        viajero = Viajero.query.filter_by(user_id = search_user.id).one_or_none()

    if search_user.password == password:
        return jsonify({ 
            "token" : create_access_token(identity=search_user.username),
            "user" : search_user.username,
            "rol" : search_user.rol,
            "idUser" : search_user.id,
            "idAgencia" : agencia.id if (agencia != None and agencia.id != "" ) else "",
            "idViajero" : viajero.id if (viajero != None and viajero.id != "" ) else "",
        }), 200
    #handling errors
    return jsonify({ "message" : "password doesnt match, be carefull 🔓️ "}), 401


@api.route('/user', methods=['POST'])
def new_user():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        nuevo_user = User(body['username'], body['email'], body['password'], body['rol'])
        # nuevo_user = User(body['username'], body['email'], body['password'], body['rol'], body['is_active'])
        print(nuevo_user)
        db.session.add(nuevo_user)
        db.session.commit()
        return jsonify(nuevo_user.serialize()), 200
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
    
@api.route('/agency', methods=['POST'])
def new_agency():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        nuevo_agency = Agencia(body['name'], body['rif'], body['phone'], body['user_id'])
        # nuevo_user = User(body['username'], body['email'], body['password'], body['rol'], body['is_active'])
        print(nuevo_agency)
        db.session.add(nuevo_agency) # Memoria RAM de SQLAlchemy
        db.session.commit() # Inserta el nuevo_piso en la BD de psql ✅
        return jsonify(nuevo_agency.serialize()), 200 #Piso searilzado
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    
@api.route('/viajero', methods=['POST'])
def new_viajero():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        nuevo_viajero = Viajero(body['type_person'], body['cedula'], body['name'], 
                                body['lastname'], body['dates_of_birth'], body['phone'], body['user_id'])
        print(nuevo_viajero)
        db.session.add(nuevo_viajero) # Memoria RAM de SQLAlchemy
        db.session.commit() # Inserta el nuevo_piso en la BD de psql ✅
        return jsonify(nuevo_viajero.serialize()), 200 #Piso searilzado
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500


@api.route('/new-package', methods=['POST'])
@jwt_required
def new_package():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        new_package = PaqueteDeViaje(body['title'], body['destination'], body['starting_location'], 
                                     body['start_date'], body['finish_date'], body['includes'], 
                                     body['type_of_transport'], body['type_of_accommodation'], body['description'], 
                                     body['max_travellers'], body['reservation_cost'], body['total_cost'], 
                                     body['agencia_id'] )
        print(new_package)
        db.session.add(new_package) # Memoria RAM de SQLAlchemy
        db.session.commit() # Inserta el nuevo_piso en la BD de psql ✅
        return jsonify(new_package.serialize()), 200 #Piso searilzado
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500
    

@api.route('/user-info', methods=['PUT'])
def get_infoUser():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        infoUser = User.query.filter_by(id = body['idUser']).one_or_none()

        return jsonify(infoUser.serialize()), 200
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

@api.route('/agency-info', methods=['PUT'])
def get_infoAgency():
    body = request.json #lo que viene del request como un dic de python 🦎
    try:
        infoAgency = Agencia.query.filter_by(id = body['idAgencia']).one_or_none()

        return jsonify(infoAgency.serialize()), 200
    except Exception as err:
        return jsonify({ "message" : "Ah ocurrido un error inesperado ‼️" + str(err)}), 500

