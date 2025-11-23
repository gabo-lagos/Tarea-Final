from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from conection_with_mongo.conection_MongoDB import usuarios_col

auth_bp = Blueprint("auth_bp", __name__)

# -------------------------
#  LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = usuarios_col.find_one({"username": data["username"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

    token = create_access_token(
        identity=user["username"],
        additional_claims={"role": user["role"]}
    )

    return jsonify({"access_token": token, "role": user["role"]})


# -------------------------
#  CREAR USUARIO (solo admin)
# -------------------------
from flask_jwt_extended import jwt_required, get_jwt

def role_required(roles):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"msg": "No autorizado"}), 403
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator


@auth_bp.route("/register", methods=["POST"])
@role_required(["admin"])
def register_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({"msg": "Se requiere username, password y role"}), 400

    if usuarios_col.find_one({"username": data["username"]}):
        return jsonify({"msg": "El usuario ya existe"}), 409

    usuarios_col.insert_one({
        "username": data["username"],
        "password": generate_password_hash(data["password"]),
        "role": data["role"]
    })

    return jsonify({"msg": "Usuario creado exitosamente"}), 201