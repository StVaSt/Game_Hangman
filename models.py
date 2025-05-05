from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import db

# Модель таблицы users_hangman
class UsersHangman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    count_win = db.Column(db.Integer, default=0)
    count_loss = db.Column(db.Integer, default=0)

# Модель таблицы words_hangman
class WordsHangman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(15), nullable=False)
    count_letter = db.Column(db.Integer, nullable=False)
    count_win = db.Column(db.Integer, default=0)
    count_loss = db.Column(db.Integer, default=0)
    description = db.Column(db.String(255), nullable=False)

# Модель таблицы cookies_hangman
class CookiesHangman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), ForeignKey('users_hangman.login'), nullable=False)
    cookie_value = db.Column(db.String(255), nullable=False)
    validity_period = db.Column(db.DateTime, nullable=False)

    user = relationship('UsersHangman', backref=db.backref('cookies', lazy=True))

