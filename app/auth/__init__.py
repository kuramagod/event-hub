from flask import Blueprint

from .services import get_current_user, login_required

bp = Blueprint("auth", __name__, url_prefix="/auth")


from . import routes
