from flask import render_template

errors = {
    "existing login": "Пользователь с таким именем уже существует",
    "the wrong username": "Логин должен быть от 5 до 15 символов",
    "the wrong password": "Пароль должен быть от 5 до 10 символов и должен состоять из цифр и латинских букв",
    "username does not exist": "Пользователя с таким именем не существует",
    "incorrect password": "Неверный пароль для данного пользователя",
    "existing word": "Такое слово уже существует",
    "the wrong word": "Слово должно быть от 5 до 15 символов",
    "cookie error": "Необходима авторизация"}

def cookie_error_template(error_name):
    return render_template("authorization.html", error=errors[error_name])

def add_word_error_template(error_name):
    return render_template("add_word.html", error=errors[error_name])

def authorization_error_template(error_name):
    return render_template("authorization.html", error=errors[error_name])

def registration_error_template(error_name):
    return render_template("registration.html", error=errors[error_name])