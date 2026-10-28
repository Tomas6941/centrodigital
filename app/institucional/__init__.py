from flask import Blueprint

bp = Blueprint('institucional', __name__)

from . import routes
