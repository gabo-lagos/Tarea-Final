
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client["flask_jwt_db"]
    juguetes_col = db["juguetes"]
    usuarios_col = db["usuarios"]
    print("Conectado correctamente a MongoDB")
except Exception as e:
    print("No se pudo conectar a MongoDB:", e)
    client = None
    db = None
    juguetes_col = None
    usuarios_col = None
