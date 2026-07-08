from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, ValidationError
from app.db import db_session
from app.models import User
from werkzeug.security import check_password_hash
from app.validators import validate_unique_field


class RegisterationForm(FlaskForm):
    fullname = StringField('ФИО', validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=50, message="Длина поля должна быть от 4 до 50 символов") 
    ])
    
    email = StringField('E-mail', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=35, message="Длина поля должна быть от 6 до 35 символов"),
        validators.Email(message="Неверный синтаксис почты"),
        validate_unique_field(User, User.email, "Email уже зарегистрирован")
    ])
    
    phone = StringField('Телефон', validators=[
        validators.Length(min=10, max=15, message="Длина поля должна быть от 6 до 15 символов"), 
        validate_unique_field(User, User.phone, "Телефон уже зарегистрирован"), 
        validators.Regexp('^(\+7|7|8)?\d{10}$', message="Неверный синтаксис номера, введите российский стандарт")
    ])
    
    password = PasswordField('Пароль',  validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=35, message="Длина поля должна быть от 6 до 35 символов"), 
    ]) 


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[
        validators.DataRequired(message="E-mail обязателен"),
        validators.Email(message="Неверный синтаксис почты"),
    ])
    
    password = PasswordField('Пароль',  validators=[
        validators.DataRequired(message="Пароль обязателен"),
    ])

    def validate_password(self, field):
        user = db_session.query(User).filter_by(email=self.email.data).first()
        
        if not user:
            raise ValidationError("Пользователь с таким email не найден")
        
        if not check_password_hash(user.password_hash, field.data):
            raise ValidationError("Неверный пароль")
        
        self.user = user