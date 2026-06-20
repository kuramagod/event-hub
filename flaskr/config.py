import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = "e0f347f9cf4616503604b40bf0c4e66b73b330872fae7d45b5c0f254994f840f" # TODO спрячь секрет кей
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR.parent / "instance" / "flaskr.sqlite"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False