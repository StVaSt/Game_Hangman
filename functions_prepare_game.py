from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersHangman, WordsHangman, CookiesHangman
from flask import request, render_template, make_response
from datetime import datetime, timedelta
from functions_process_game import process_play
import random
import string
import re
from database import db


errors = {
    "existing_login": "Пользователь с таким именем уже существует",
    "the wrong username": "Логин должен быть от 5 до 15 символов",
    "the wrong password": "Пароль должен быть от 5 до 10 символов и должен состоять из цифр и латинских букв",
    "username_does_not_exist": "Пользователя с таким именем не существует",
    "incorrect password": "Неверный пароль для данного пользователя",
    "existing_word": "Такое слово уже существует",
    "the wrong word": "Слово должно быть от 5 до 15 символов",
    "you need to log in": "Необходима авторизация"}

def register_user(login, password):
    existing_user = UsersHangman.query.filter_by(login=login).first()
    if existing_user:
        return render_template("registration.html", error=errors["existing_login"])

    if not 5 <= len(login) <= 15:
        return render_template("registration.html", error=errors["the wrong username"])

    if not (5 <= len(password) <= 10) or not (re.search(r'[A-Za-z]', password) and re.search(r'\d', password)):
        return render_template("registration.html", error=errors["the wrong password"])

    password = generate_password_hash(request.form['pass'])

    new_user = UsersHangman(login=login, password=password)

    db.session.add(new_user)
    db.session.commit()

    return render_template("registration_ok.html")

def authorize_user(login, password):
    existing_user = UsersHangman.query.filter_by(login=login).first()
    if not existing_user:
        return render_template("authorization.html", error=errors["username_does_not_exist"])

    if existing_user and not check_password_hash(existing_user.password, password):
        return render_template("authorization.html", error=errors["incorrect password"])

    cookie_value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    response = make_response(render_template("authorization_ok.html", authorized_user=login))
    response.set_cookie("user_login", cookie_value, max_age=60*60*24*5)

    validity_period = datetime.now() + timedelta(days=5)

    cookie_user = CookiesHangman(login=login, cookie_value=cookie_value, validity_period=validity_period)

    db.session.add(cookie_user)
    db.session.commit()

    return response

def add_new_word(word, description):
    existing_word = WordsHangman.query.filter_by(word=word).first()
    if existing_word:
        return render_template("add_word.html", error=errors["existing_word"])

    if not 5 <= len(word) <= 15:
        return render_template("add_word.html", error=errors["the wrong word"])

    new_word = WordsHangman(word=word, count_letter=len(word), description=description)

    db.session.add(new_word)
    db.session.commit()

    return render_template("add_word_ok.html")

def check_cookie(route, value_cookie_client):
    if not value_cookie_client:
        return render_template("authorization.html", error=errors["you need to log in"])

    cookie_database = CookiesHangman.query.filter_by(cookie_value=value_cookie_client).first()

    if not cookie_database:
        return render_template("authorization.html", error=errors["you need to log in"])

    validity_period = cookie_database.validity_period
    login = cookie_database.login

    current_time = datetime.now()

    if validity_period <= current_time:
        return render_template("authorization.html", error=errors["you need to log in"])

    if route == "main_game":
        return process_main_game()
    elif route == "statistics":
        return process_statistics(login)
    elif route == "add_word":
        return process_add_word()
    elif route == "play":
        return process_play(login)


def process_main_game():
    return render_template("main_game.html")

def process_statistics(login):
    login_database_users = UsersHangman.query.filter_by(login=login).first()
    count_win = login_database_users.count_win
    count_loss = login_database_users.count_loss
    total = count_win + count_loss
    return render_template("statistics.html", authorized_user=login, total=total, count_win=count_win, count_loss=count_loss)

def process_add_word():
    return render_template("add_word.html")


