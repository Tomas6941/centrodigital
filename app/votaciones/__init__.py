from flask import Blueprint

bp = Blueprint('votaciones', __name__, url_prefix='/votaciones')

from . import routes
