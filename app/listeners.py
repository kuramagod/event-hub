from sqlalchemy import event, select
from slugify import slugify

from app.models import Event
from app.db import db_session


@event.listens_for(Event, "before_insert")
def create_slug(mapper, connection, target):
    if target.slug:
        return

    base_slug = slugify(target.name)
    slug = base_slug
    counter = 1

    while db_session.query(Event).filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    target.slug = slug