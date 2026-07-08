import functools

from flask import redirect, session, url_for 
from app.db import db_session
from app.models import User


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if user_id:
        return db_session.query(User).get(user_id)
    return None