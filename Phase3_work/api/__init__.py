# api/__init__.py
import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# ---- PATH SETUP ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Phase2_work"))
sys.path.insert(0, BASE_DIR)
PHASE2_ROOT = os.path.abspath(BASE_DIR)

# ---- LOAD ENV VARS ----
# Explicitly load the .env from Phase2_work
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# --- ENV VARS ----
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = "F8F6iVoAlcXnLPll" #os.getenv("GG_PASS", "")

# ---- UTIL IMPORTS ----
from src.user_functions.users_operations import (
    create_user_entity,
    update_users_fields,
    update_users_email,
    update_users_password,
    get_password_hashed,
    UserOperationError,
)
from src.user_functions.view_based_operations import Role
from src.utils.logging_utils import log_info, log_error


def create_app():
    print(MYSQL_PASS)
    print("^")
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "dev-secret-key-change-this"  # TODO get rid of this

    # Allow common frontend dev origins (Vite default 5173, CRA 3000) for development
    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_headers=["Content-Type", "Authorization"]
    )
    JWTManager(app)

    from api.auth import auth_bp
    from api.public import public_bp
    from api.user import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(public_bp, url_prefix="/api/public")
    app.register_blueprint(user_bp, url_prefix="/api/user")

    return app
