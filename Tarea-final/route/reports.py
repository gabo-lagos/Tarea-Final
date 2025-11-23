from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from conection_with_mongo.conection_MongoDB import usuarios_col, db

reports_bp = Blueprint("reports_bp", __name__)

def role_required(roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"msg": "No autorizado"}), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper


@reports_bp.route("/", methods=["GET"])
@role_required(["manager", "admin"])
def reports():
    return jsonify({"msg": "Datos de reporte confidenciales"}), 200

@reports_bp.route("/migrar_usuarios", methods=["POST"])
@role_required(["admin"])
def migrar_usuarios():
    try:
        if db is None or usuarios_col is None:
            return jsonify({"msg": "MongoDB no está disponible"}), 503

        existentes = [
            u["username"] for u in usuarios_col.find({}, {"username": 1, "_id": 0})
        ]

        nuevos = []
        default_users = {
            "alice": {"password": "1234", "role": "client"},
            "bob": {"password": "1234", "role": "manager"},
            "carol": {"password": "1234", "role": "admin"},
        }

        for username, data in default_users.items():
            if username not in existentes:
                nuevos.append(
                    {
                        "username": username,
                        "password": data["password"],
                        "role": data["role"],
                    }
                )

        if not nuevos:
            return jsonify({"msg": "No hay nuevos usuarios para migrar"}), 200

        result = usuarios_col.insert_many(nuevos)

        return (
            jsonify(
                {"msg": f"Se migraron {len(result.inserted_ids)} usuarios a MongoDB"}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"msg": "Error al migrar usuarios", "error": str(e)}), 500
