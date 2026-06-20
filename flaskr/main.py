from flask import Blueprint, redirect, url_for
from flaskr.auth import get_current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    user = get_current_user()
    if user:
        return redirect(url_for('event.index'))
    return redirect(url_for('auth.login'))