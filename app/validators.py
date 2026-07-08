from wtforms import ValidationError
from app.db import db_session


def validate_unique_field(model, column, message=None):
    def validate(form ,field):
        if not field.data:
            return
        if db_session.query(model).filter(column == field.data).first():
            if message:
                raise ValidationError(message or f"{field.label.text} уже существует")
    return validate