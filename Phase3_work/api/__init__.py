# api/__init__.py
'''
    File: api/__init__.py

    Author: Colby Wirth

    Version: 8 December 2025

    Description:
        This file implements the Flask application factory for the GrantGuru API. 
        It sets up the Flask app, configures CORS, and initializes JWT-based authentication 
        to manage user sessions in a stateless manner.

    JWT Authentication:
        - Upon user login, the server generates a signed JSON Web Token (JWT) that encodes 
          the user's UUID.
        - The token is signed using a secure 32-byte secret key 
        - Tokens are stored in session storage
        - When the server receives a request with a JWT, it verifies the signature and extracts 
          the UUID to authorize access to only the requesting user's data.
'''
import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import secrets

# ---- PATH SETUP ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Phase2_work"))
sys.path.insert(0, BASE_DIR)
PHASE2_ROOT = os.path.abspath(BASE_DIR)

dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

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


DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "admin")
MYSQL_PASS = os.getenv("GG_PASS", "admin")



# retrieving/(generating jwt secret key if needed)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if JWT_SECRET_KEY is None:
    JWT_SECRET_KEY = secrets.token_hex(32)
    with open(dotenv_path, "a") as f:
        f.write(f"JWT_SECRET_KEY={JWT_SECRET_KEY}\n")



def create_app():

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://localhost:3000",
        ],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    JWTManager(app)

    from api.auth import auth_bp
    from api.public import public_bp
    from api.user import user_bp
    from api.applications import applications_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(public_bp, url_prefix="/api/public")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(applications_bp, url_prefix="/api/applications")

    return app
