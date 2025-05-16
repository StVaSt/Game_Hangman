from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersHangman, WordsHangman, CookiesHangman
from flask import request, render_template
from datetime import datetime, timedelta
from functions_process_game import process_play
import random
import string
import re
from database import db
from error_templates import cookie_error_template, add_word_error_template, authorization_error_template, registration_error_template
from ok_templates import registration_ok, authorization_ok, add_word_ok



# === Функция register_user и вытекающие из нее===
def register_user(login, password):
    existing_user = search_registration_login(login)
    if existing_user:
        return registration_error_template("existing login")

    if not 5 <= len(login) <= 15:
        return registration_error_template("the wrong username")

    if not (5 <= len(password) <= 10) or not (re.search(r'[A-Za-z]', password) and re.search(r'\d', password)):
        return registration_error_template("the wrong password")

    password = password_generation()

    add_user(login, password)

    return registration_ok()

def search_registration_login(login):
    existing_user = UsersHangman.query.filter_by(login=login).first()
    return existing_user

def password_generation():
    password = generate_password_hash(request.form['pass'])
    return password

def add_user(login, password):
    new_user = UsersHangman(login=login, password=password)
    db.session.add(new_user)
    db.session.commit()




# === Функция authorize_user и вытекающие из нее===
def authorize_user(login, password):
    existing_user = search_authorization_login(login)
    if not existing_user:
        return authorization_error_template("username does not exist")

    verification_result = check_pass(existing_user, password)

    if existing_user and not verification_result:
        return authorization_error_template("incorrect password")

    cookie_value = value_generating()

    validity_period = datetime.now() + timedelta(days=5)

    add_cookie(login, cookie_value, validity_period)

    return authorization_ok(login, cookie_value)

def search_authorization_login(login):
    existing_user = UsersHangman.query.filter_by(login=login).first()
    return existing_user

def check_pass(existing_user, password):
    password = check_password_hash(existing_user.password, password)
    return password

def value_generating():
    value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return value

def add_cookie(login, cookie_value, validity_period):
    cookie_user = CookiesHangman(login=login, cookie_value=cookie_value, validity_period=validity_period)
    db.session.add(cookie_user)
    db.session.commit()




# === Функция add_new_word и вытекающие из нее===
def add_new_word(word, description):
    existing_word = word_search(word)
    if existing_word:
        return add_word_error_template("existing word")

    if not 5 <= len(word) <= 15:
        return add_word_error_template("the wrong word")

    add_word(word, description)

    return add_word_ok()

def word_search(word):
    existing_word = WordsHangman.query.filter_by(word=word).first()
    return existing_word

def add_word(word, description):
    new_word = WordsHangman(word=word, count_letter=len(word), description=description)
    db.session.add(new_word)
    db.session.commit()




# === Функция check_cookie и вытекающие из нее===
def check_cookie(route, cookie_from_client):
    if not cookie_from_client:
        return cookie_error_template("cookie error")

    cookie_from_database = get_cookie_from_database(cookie_from_client)

    if not cookie_from_database:
        return cookie_error_template("cookie error")

    validity_period = get_validity_period(cookie_from_database)
    login = get_login(cookie_from_database)

    current_time = datetime.now()

    if validity_period <= current_time:
        return cookie_error_template("cookie error")

    if route == "main_game":
        return process_main_game()
    elif route == "statistics":
        return process_statistics(login)
    elif route == "add_word":
        return process_add_word()
    elif route == "play":
        return process_play(login)

def get_cookie_from_database(cookie_from_client):
    cookie_from_database = CookiesHangman.query.filter_by(cookie_value=cookie_from_client).first()
    return cookie_from_database

def get_validity_period(cookie_from_database):
    validity_period = cookie_from_database.validity_period
    return validity_period

def get_login(cookie_from_database):
    login = cookie_from_database.login
    return login

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


