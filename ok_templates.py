from flask import render_template
from flask import make_response


def registration_ok():
    return render_template("registration_ok.html")

def authorization_ok(login, cookie_value):
    response = make_response(render_template("authorization_ok.html", authorized_user=login))
    response.set_cookie("user_login", cookie_value, max_age=60*60*24*5)
    return response

def add_word_ok():
    return render_template("add_word_ok.html")