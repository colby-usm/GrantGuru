import os
import sys
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import routes_auth

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../Phase2_work"))
sys.path.insert(0, BASE_DIR)
PHASE2_ROOT = os.path.abspath(os.path.join(BASE_DIR))
