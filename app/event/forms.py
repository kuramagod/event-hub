from flask_wtf import FlaskForm
from wtforms import StringField, validators, URLField, DateField, TimeField, IntegerField, TextAreaField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Category, City


class EventForm(FlaskForm):
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

    price = IntegerField("Укажите цену", validators=[
        validators.Optional()
    ])

    external_url = URLField("Ссылка на внеший ресурс", validators=[
        validators.URL(),
        validators.Optional()
    ])

    description = TextAreaField("Описание", validators=[
        validators.DataRequired(),
        validators.Length(max=500, message="Длина поля должна быть до 500 символов")
    ])


class DeleteForm(FlaskForm):
    submit = SubmitField("Удалить")