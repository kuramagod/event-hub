from flask import redirect, url_for

from app.auth.services import get_current_user
from . import bp


@bp.route('/')
def index():
    user = get_current_user()
    if user:
        return redirect(url_for('event.index'))
    return redirect(url_for('auth.login'))
