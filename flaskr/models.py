import re
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from slugify import slugify
from .db import Base, db_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), unique=False)
    email = Column(String(120), unique=True)
    phone = Column(String(50), unique=True)
    password_hash = Column(String(255), unique=False)

    events = relationship("Event", back_populates="author")
    favorite = relationship("Favorite", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<Пользователь {self.fullname!r}>'


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)

    events = relationship("Event", back_populates="category")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<Категория {self.name!r}>'


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)

    events = relationship("Event", back_populates="city")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<Город {self.name!r}>'


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=False)
    slug = Column(String(120), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='SET NULL'))
    image_url = Column(String(50), unique=False)
    city_id = Column(Integer, ForeignKey('city.id', ondelete='SET NULL'))
    address = Column(String(200), unique=False)
    date = Column(DateTime, nullable=False)
    price = Column(String(50), unique=False)
    description = Column(String(500), unique=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    author = relationship("User", back_populates="events")
    category = relationship("Category", back_populates="events")
    city = relationship("City", back_populates="events")
    favorites = relationship("Favorite", back_populates="event")

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
            counter = 1
            while Event.query.filter_by(slug=self.slug).first():
                self.slug = f"{self.slug}-{counter}"
                counter += 1
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return f'<Мероприятие {self.name!r}>'


class Favorite(Base):
    __tablename__ = 'favorities'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'))

    user = relationship("User", back_populates="favorite")
    event = relationship("Event", back_populates="favorites")

    def __init__(self, user=None, event=None):
        self.user = user
        self.event = event

    def __repr__(self):
        return f'<Добавлен в избранное у {self.user!r}>'
