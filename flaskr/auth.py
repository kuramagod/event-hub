import functools

from flask import Blueprint, redirect, render_template, request, session, url_for 

from flaskr.db import db_session
from flaskr.models import User
from flaskr.forms import RegisterationForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


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


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterationForm()
    if request.method == "POST" and form.validate():
        user = User(fullname=form.fullname.data, email=form.email.data, phone=form.phone.data)
        user.set_password(password=form.password.data)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        session["user_id"] = form.user.id
        session["logged_in"] = True
        return redirect(url_for("event.index"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
