from flask import Flask, render_template, request
from functions_prepare_game import register_user, authorize_user, check_cookie, add_new_word
from models import db
from functions_process_game import guessing
import json


app = Flask(__name__)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Подключения к БД

app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']

app.secret_key = config['secret']['key']

# Инициализация объекта db
db.init_app(app)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/new_users", methods=["POST"])
def new_users():
    login = request.form['login']
    password = request.form['pass']
    return register_user(login, password)

@app.route("/authorization")
def authorization():
    return render_template("authorization.html")

@app.route("/login_users", methods=["POST"])
def login_users():
    login = request.form['login']
    password = request.form['pass']
    return authorize_user(login, password)

@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/main_game")
def main_game():
    value_cookie_client = request.cookies.get("user_login")
    return check_cookie("main_game", value_cookie_client)

@app.route("/add_word")
def add_word():
    value_cookie_client = request.cookies.get("user_login")
    return check_cookie("add_word",value_cookie_client)

@app.route("/new_word", methods=["POST"])
def new_word():
    word = request.form['word'].strip().capitalize()
    description = request.form['description'].strip().capitalize()
    return add_new_word(word, description)

@app.route("/statistics")
def statistics():
    value_cookie_client = request.cookies.get("user_login")
    return check_cookie("statistics", value_cookie_client)

@app.route("/play")
def play():
    value_cookie_client = request.cookies.get("user_login")
    return check_cookie("play", value_cookie_client)

@app.route("/guess", methods=["POST"])
def guess():
    letter = request.form['letter']
    return guessing(letter)


if __name__ == '__main__':
    app.run(debug=True)
