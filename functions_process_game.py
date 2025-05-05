from models import WordsHangman, UsersHangman
from flask import render_template, url_for, session
from session import GameSessionData
from database import db
import random

def process_play(login):
    game_data = GameSessionData()
    game_data.reset()
    game_data.login = login
    game_data.save()
    data = get_data()
    return render_template(
        "play.html",
        authorized_user=login,
        count_letter=data["count_letter"],
        empty_element=data["empty_element"],
        description=data["description"],
        count_win=data["count_win"],
        count_loss=data["count_loss"],
        image_num=data["image_num"]
    )

def get_data():
    random_word = get_random_word()
    game_data = GameSessionData()
    game_data.word = random_word.word
    game_data.count_letter = random_word.count_letter
    game_data.description = random_word.description
    game_data.count_win = random_word.count_win
    game_data.count_loss = random_word.count_loss
    game_data.try_win = 0
    game_data.try_loss = 0
    game_data.image_num = url_for('static', filename=f'{game_data.try_loss}.png')
    game_data.empty_element =  " _ " * len(game_data.word)
    game_data.save()
    return {
        "word": game_data.word,
        "count_letter": game_data.count_letter,
        "description": game_data.description,
        "count_win": game_data.count_win,
        "count_loss": game_data.count_loss,
        "image_num": game_data.image_num,
        "try_win": game_data.try_win,
        "try_loss": game_data.try_loss,
        "empty_element": game_data.empty_element
    }

def get_random_word():
    word = db.session.query(WordsHangman).all()
    if word:
        return random.choice(word)
    else:
        return None


def guessing(letter):
    game_data = GameSessionData()

    if letter in game_data.word:
        positions = [i for i in range(len(game_data.word)) if game_data.word[i] == letter]
        game_data.try_win +=1

        updated_empty_element = list(game_data.empty_element.replace(" ", ""))

        for pos in positions:
            updated_empty_element[pos] = letter
        if all(item.isalpha() for item in updated_empty_element):
            word_data = WordsHangman.query.filter_by(word=game_data.word).first()
            word_data.count_win += 1
            login_data = UsersHangman.query.filter_by(login=game_data.login).first()
            login_data.count_win += 1
            db.session.commit()
            return render_template("win.html", image_num=game_data.image_num, try_win=game_data.try_win+game_data.try_loss)
        else:
            game_data.empty_element =" ".join(updated_empty_element)
    else:
        game_data.try_loss +=1
        if game_data.try_loss == 7:
            word_data = WordsHangman.query.filter_by(word=game_data.word).first()
            word_data.count_loss += 1
            login_data = UsersHangman.query.filter_by(login=game_data.login).first()
            login_data.count_loss += 1
            db.session.commit()
            game_data.image_num = url_for('static', filename=f'{game_data.try_loss}.png')
            return render_template("game_over.html", image_num=game_data.image_num)
        else:
            game_data.image_num = url_for('static', filename=f'{game_data.try_loss}.png')

    if letter not in session.get('used_letters', []):
        session.setdefault('used_letters', []).append(letter)
    game_data.save()
    return render_template(
        "play.html",
        authorized_user=game_data.login,
        count_letter=game_data.count_letter,
        empty_element=game_data.empty_element,
        description=game_data.description,
        count_win=game_data.count_win,
        count_loss=game_data.count_loss,
        image_num=game_data.image_num
    )

