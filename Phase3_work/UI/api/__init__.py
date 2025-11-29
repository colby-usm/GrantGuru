# api/__init__.py
from flask import Flask
from flask_cors import CORS

from api.auth import auth_bp
from api.public import public_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(public_bp, url_prefix="/api/public")

