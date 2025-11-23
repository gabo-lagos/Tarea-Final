
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from conection_with_mongo.conection_MongoDB import db, juguetes_col

juguetes_bp = Blueprint('juguetes_bp', __name__)

juguetes = [
    {
        "id": 1,
        "nombre": "Porsche 917LH",
        "categoria": "Carros",
        "edad_recomendada": "3+",
        "precio": 10000.0,
        "marca": "Hot Wheels"
    },
    {
        "id": 2,
        "nombre": "Aston Martin DB4GT",
        "categoria": "Carros",
        "edad_recomendada": "3+",
        "precio": 10000.0,
        "marca": "Hot Wheels"
    },
    {
        "id": 3,
        "nombre": "Hot Wheels NIGHTBURNERZ",
        "categoria": "Paquetes de carros",
        "edad_recomendada": "3+",
        "precio": 54900.0,
        "marca": "Hot Wheels"
    },
    {
        "id": 4,
        "nombre": "Monoplaza Ferrari F1",
        "categoria": "Carros a escala",
        "edad_recomendada": "6+",
        "precio": 20000.0,
        "marca": "LEGO"
    },
    {
        "id": 5,
        "nombre": "Pelota de futbol",
        "categoria": "Deportes",
        "edad_recomendada": "7+",
        "precio": 160000.0,
        "marca": "Adidas"
    }
]



def role_required(allowed_roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            role = claims.get('role')
            if role not in allowed_roles:
                return jsonify({"msg": "El usuario no tiene el rol requerido"}), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper


@juguetes_bp.route('/', methods=['GET'])
def get_all_juguetes():

    categoria = request.args.get('categoria')
    marca = request.args.get('marca')

    resultados = juguetes

    if categoria:
        resultados = [j for j in resultados if j["categoria"].lower() == categoria.lower()]
    if marca:
        resultados = [j for j in resultados if j["marca"].lower() == marca.lower()]

    return jsonify(resultados)


@juguetes_bp.route('/', methods=['POST'])
@jwt_required()
def add_juguete():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Falta el cuerpo JSON"}), 400
    data["id"] = (juguetes[-1]['id'] + 1) if juguetes else 1
    juguetes.append(data)
    return jsonify(data), 201


@juguetes_bp.route('/<int:id>', methods=['DELETE'])
@role_required(['manager', 'admin'])
def delete_juguete(id):
    global juguetes
    encontrado = [j for j in juguetes if j['id'] == id]
    if not encontrado:
        return jsonify({"error": "Juguete no encontrado"}), 404
    juguetes = [j for j in juguetes if j['id'] != id]
    return jsonify({"mensaje": f"Juguete con ID {id} eliminado"}), 200
hola