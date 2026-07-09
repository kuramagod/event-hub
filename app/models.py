from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from .db import Base


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"Роль: {self.name}" if self.name else "Роль"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), unique=False)
    email = Column(String(120), unique=True)
    phone = Column(String(50), unique=True)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='SET NULL'))
    password_hash = Column(String(255), unique=False)
    
    role = relationship("Role", back_populates="users")
    events = relationship("Event", back_populates="author")
    favorite = relationship("Favorite", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Пользователь: {self.fullname}" if self.fullname else "Пользователь"


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    color = Column(String, unique=False, nullable=True)

    events = relationship("Event", back_populates="category")

    def __repr__(self):
        return f"Категория: {self.name}" if self.name else "Категория"


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)

    events = relationship("Event", back_populates="city")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f"Город: {self.name}" if self.name else "Город"


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=False)
    slug = Column(String(120), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='SET NULL'))
    image_url = Column(String(550), unique=False)
    city_id = Column(Integer, ForeignKey('city.id', ondelete='SET NULL'))
    address = Column(String(200), unique=False)
    date = Column(DateTime, nullable=False)
    price = Column(String(50), unique=False, nullable=True)
    description = Column(String(500), unique=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    external_url = Column(String, unique=False, nullable=True)

    author = relationship("User", back_populates="events")
    category = relationship("Category", back_populates="events")
    city = relationship("City", back_populates="events")
    favorites = relationship("Favorite", back_populates="event")

    def __repr__(self):
        return f"Мероприятие: {self.name}" if self.name else "Мероприятие"


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
        return f"Избранное: {self.user}" if self.user else "Избранное"
