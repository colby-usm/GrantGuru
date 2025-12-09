from flask import Blueprint

applications_bp = Blueprint('applications', __name__)

from . import routes_applications
from . import routes_backup
