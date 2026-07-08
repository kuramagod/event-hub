from . import bp
from flask import redirect, render_template, request, session, url_for 

from app.db import db_session
from app.models import User
from .forms import RegisterationForm, LoginForm


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