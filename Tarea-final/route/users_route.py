from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash
from conection_with_mongo.conection_MongoDB import db, usuarios_col
from route.auth_route import role_required

users_bp = Blueprint('users_bp', __name__)

users = {
    'alice': {'password': generate_password_hash('alicepass'), 'role': 'client'},
    'bob': {'password': generate_password_hash('bobpass'), 'role': 'manager'},
    'carol': {'password': generate_password_hash('carolpass'), 'role': 'admin'}
}

@users_bp.route("/", methods=["GET"])
@role_required(["manager", "admin"])
def reports():
    return jsonify({"msg": "Datos de reporte confidenciales"}), 200


@users_bp.route("/migrar_usuarios", methods=["POST"])
@role_required(["admin"])
def migrar_usuarios():
    try:
        if db is None or usuarios_col is None:
            return jsonify({"msg": "MongoDB no está disponible"}), 503

        existentes = [u["username"] for u in usuarios_col.find({}, {"username": 1, "_id": 0})]
        nuevos = []

        for username, data in users.items():
            if username not in existentes:
                nuevos.append({
                    "username": username,
                    "password": data["password"],
                    "role": data["role"]
                })

        if not nuevos:
            return jsonify({"msg": "No hay nuevos usuarios para migrar"}), 200

        result = usuarios_col.insert_many(nuevos)
        return jsonify({"msg": f"Se migraron {len(result.inserted_ids)} usuarios a MongoDB"}), 201

    except Exception as e:
        return jsonify({"msg": "Error al migrar usuarios", "error": str(e)}), 500

@users_bp.route("/usuarios", methods=["GET"])
@role_required(["admin"])
def get_users():
    data = list(usuarios_col.find({}, {"_id": 0, "password": 0}))
    return jsonify(data), 200
