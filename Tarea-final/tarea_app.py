from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os
from route.auth_route import auth_bp
from route.users_route import users_bp
from route.juguetes_route import juguetes_bp
from route.users_route import users_bp
from route.panel_route import panel_bp
from route.reports import reports_bp

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(juguetes_bp, url_prefix="/juguetes")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(panel_bp, url_prefix="/panel")


if __name__ == "__main__":
    app.run(port=int(os.getenv("FLASK_PORT", 8003)), debug=True)

