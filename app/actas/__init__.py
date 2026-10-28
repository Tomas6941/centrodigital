from flask import Blueprint

bp = Blueprint('actas', __name__, url_prefix='/actas')

from . import routes
