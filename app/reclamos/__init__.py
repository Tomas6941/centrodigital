from flask import Blueprint

bp = Blueprint('reclamos', __name__, url_prefix='/reclamos')

from . import routes
