from wtforms import Form, StringField, PasswordField, validators, ValidationError, URLField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskr.db import db_session
from flaskr.models import User, Category, City
from werkzeug.security import check_password_hash


def validate_unique_field(model, column, message=None):
    def validate(form ,field):
        if not field.data:
            return
        if db_session.query(model).filter(column == field.data).first():
            if message:
                raise ValidationError(message)
            else:
                raise ValidationError(f"{field.label.text} уже существует")
    return validate


class RegisterationForm(Form):
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


class LoginForm(Form):
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


class EventForm(Form):
    name = StringField("Название", validators=[
        validators.DataRequired(message="Название обязательно"),
        validators.Length(max=120, message="Длина поля должна быть до 120 символов"),
    ])
    
    category = QuerySelectField(
        'Категория', 
        query_factory=lambda: Category.query.all(),
        get_label='name',
        allow_blank=False
    )
    
    image_url = URLField("URL Обложки", validators=[
        validators.DataRequired()
    ])

    city = QuerySelectField(
        'Город',
        query_factory=lambda: City.query.all(),
        get_label='name',
        allow_blank=False
    )

    address = StringField('Адрес', validators=[
        validators.DataRequired(),
        validators.Length(max=200, message="Длина поля должна быть до 200 символов")
    ])

    date = DateField("Дата", validators=[
        validators.DataRequired()
    ])

    time = TimeField("Время", validators=[
        validators.DataRequired()
    ])

    price = IntegerField("Цена(Укажите 0 если бесплатно)", validators=[
        validators.DataRequired()
    ])

    description = TextAreaField("Описание", validators=[
        validators.DataRequired(),
        validators.Length(max=500, message="Длина поля должна быть до 500 символов")
    ])


class ProfileForm(Form):    
    fullname = StringField('ФИО', validators=[
        validators.DataRequired(message="ФИО обязательно"),
        validators.Length(min=4, max=50, message="Длина поля должна быть от 4 до 50 символов") 
    ])

    phone = StringField('Телефон', validators=[
        validators.Length(min=10, max=15, message="Длина поля должна быть от 6 до 15 символов"), 
        validators.Regexp('^(\+7|7|8)?\d{10}$', message="Неверный синтаксис номера, введите российский стандарт")
    ])
    
    submit_profile = SubmitField('Сохранить изменения')

    def __init__(self, formdata=None, obj=None, user=None, **kwargs):
        super().__init__(formdata, obj, **kwargs)
        self.user = user
    
    def validate_phone(self, field):
        if not field.data:
            return
        existing_user = db_session.query(User).filter_by(phone=field.data).first()
        if existing_user and existing_user.id != self.user.id:
            raise ValidationError("Телефон уже зарегистирован")


class ChangePasswordForm(Form):
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

    def __init__(self, formdata=None, obj=None, user=None, **kwargs):
        super().__init__(formdata, obj, **kwargs)
        self.user = user
    
    def validate_old_password(self, field):
        if not self.user or not check_password_hash(self.user.password_hash, field.data):
            raise ValidationError("Старый пароль неверный")