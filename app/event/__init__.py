from flask import Blueprint

bp = Blueprint("event", __name__, url_prefix="/event")

from . import routes
