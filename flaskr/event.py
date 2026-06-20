import datetime
import re

from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort

from flaskr.auth import get_current_user, login_required
from flaskr.db import db_session
from flaskr.models import Category, City, Event, Favorite
from flaskr.forms import EventForm, ProfileForm, ChangePasswordForm

bp = Blueprint("event", __name__, url_prefix="/event")


@bp.route("/")
def index():
    categories = db_session.query(Category).all()
    cities = db_session.query(City).all()
    events = db_session.query(Event).all()
    current_user = get_current_user()

    if current_user:
        liked_event_ids = {favorite.event_id for favorite in current_user.favorite}
        for event in events:
            event.is_liked = event.id in liked_event_ids
    else:
        for event in events:
            event.is_liked = False
    return render_template(
        "event/index.html", categories=categories, cities=cities, events=events
    )


@bp.route("/<string:slug>") 
def event(slug):
    event = db_session.query(Event).filter_by(slug=slug).first()

    if not event:
        abort(404)

    current_user = get_current_user()
    
    is_liked = False
    if current_user and event:
        is_liked = any(fav.event_id == event.id for fav in current_user.favorite)

    return render_template("event/event.html", event=event, is_liked=is_liked)


@bp.route('/api/toggle-like/<int:event_id>', methods=['POST'])
@login_required
def toggle_like(event_id):
    current_user = get_current_user()
    event = db_session.query(Event).filter_by(id=event_id).first()
    if not event:
        return jsonify({'error': 'Событие не найдено'}), 404

    favorite = db_session.query(Favorite).filter_by(user_id=current_user.id, event_id=event_id).first()
    if favorite:
        db_session.delete(favorite)
        liked = False
    else:
        new_favorite = Favorite(user=current_user, event=event)
        db_session.add(new_favorite)
        liked = True

    db_session.commit()
    return jsonify({'liked': liked})


@bp.route("/add-event", methods=["GET", "POST"])
@login_required
def add_event():
    form = EventForm(request.form)
    if request.method == "POST":
        current_user = get_current_user()

        category_id = form.category.data.id if form.category.data else None
        city_id = form.city.data.id if form.city.data else None
        event_datetime = datetime.datetime.combine(form.date.data, form.time.data)
        
        event = Event(
            name=form.name.data,
            category_id=category_id,
            image_url=form.image_url.data,
            price=form.price.data,
            date=event_datetime,
            description=form.description.data,
            address=form.address.data,
            city_id=city_id,
            user_id=current_user.id,
        )
        db_session.add(event)
        db_session.commit()

        return redirect(url_for("event.index"))
    
    return render_template("event/add-event.html", form=form)


@bp.route("/collection")
@login_required
def collection():
    current_user = get_current_user()
    events = [favorite.event for favorite in current_user.favorite]
    return render_template("event/collection.html", events=events)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    current_user = get_current_user()
    profile_form = ProfileForm(request.form, user=current_user)
    change_password_form = ChangePasswordForm(request.form, user=current_user)

    if request.method == "POST":
        if profile_form.submit_profile.data and profile_form.validate():
            current_user.fullname = profile_form.fullname.data
            current_user.phone = profile_form.phone.data
            db_session.commit()
            return redirect(url_for("event.profile"))
        
        elif change_password_form.submit_password.data and change_password_form.validate():
            current_user.set_password(change_password_form.new_password.data)
            db_session.commit()
            return redirect(url_for("event.profile"))


    return render_template("event/profile.html", profile_form=profile_form, change_password_form=change_password_form)