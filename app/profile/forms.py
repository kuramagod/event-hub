from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError, SubmitField
from app.models import User
from werkzeug.security import check_password_hash
from app.db import db_session


class ProfileForm(FlaskForm):    
    fullname = StringField('ФИО', validators=[
        validators.DataRequired(message="ФИО обязательно"),
        validators.Length(min=4, max=50, message="Длина поля должна быть от 4 до 50 символов") 
    ])

    phone = StringField('Телефон', validators=[
        validators.Length(min=10, max=15, message="Длина поля должна быть от 6 до 15 символов"), 
        validators.Regexp('^(\+7|7|8)?\d{10}$', message="Неверный синтаксис номера, введите российский стандарт"),
    ])
    
    submit_profile = SubmitField('Сохранить изменения')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def validate_phone(self, field):
        if not field.data:
            return
        existing_user = db_session.query(User).filter_by(phone=field.data).first()
        if existing_user and existing_user.id != self.user.id:
            raise ValidationError("Телефон уже зарегистирован")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль',  validators=[
        validators.DataRequired(message="Старый пароль обязателен"),
        validators.Length(min=6, max=35, message="Длина поля должна быть от 6 до 35 символов"), 
    ])

    new_password = PasswordField('Новый пароль',  validators=[
        validators.DataRequired(message="Новый пароль обязателен"),
        validators.Length(min=6, max=35, message="Длина поля должна быть от 6 до 35 символов"), 
    ])

    confirm_password = PasswordField('Подтверждение пароля',  validators=[
        validators.DataRequired(message="Подтверждение пароля обязательно"),
        validators.EqualTo('new_password', message="Пароли не совпадают"),
    ])
    submit_password = SubmitField('Изменить пароль')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def validate_old_password(self, field):
        if not self.user or not check_password_hash(self.user.password_hash, field.data):
            raise ValidationError("Старый пароль неверный")