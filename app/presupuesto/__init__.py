from flask import Blueprint

bp = Blueprint('presupuesto', __name__, url_prefix='/presupuesto')

from . import routes
