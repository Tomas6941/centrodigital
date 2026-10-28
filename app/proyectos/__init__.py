from flask import Blueprint

bp = Blueprint('proyectos', __name__, url_prefix='/proyectos')

from . import routes
