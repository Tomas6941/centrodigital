from flask import Blueprint

bp = Blueprint('comunicados', __name__, url_prefix='/comunicados')

from . import routes
