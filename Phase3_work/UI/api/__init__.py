# api/__init__.py
from flask import Flask
from flask_cors import CORS
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Phase2_work"))
sys.path.insert(0, BASE_DIR)
PHASE2_ROOT = os.path.abspath(os.path.join(BASE_DIR))

from src.user_functions.users_operations import create_user_entity, get_password_hashed, UserOperationError #type: ignore
from src.user_functions.view_based_operations import Role #type: ignore
from src.utils.logging_utils import log_info, log_error # type: ignore



DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")



_ = (create_user_entity, get_password_hashed, UserOperationError, Role, log_info, log_error)

def create_app():
    app = Flask(__name__)

    CORS(app)

    from api.auth import auth_bp
    from api.public import public_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(public_bp, url_prefix="/api/public")

    return app
