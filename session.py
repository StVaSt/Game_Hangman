from flask import session

class GameSessionData:
    data_strings = ["login", "word", "description", "image_num", "empty_element"]
    data_ints = ["count_letter", "count_win", "count_loss", "try_win", "try_loss"]
    data_lists = ["used_letters"]

    def __init__(self):
        self.login = session.get("login", "")
        self.word = session.get("word", "")
        self.count_letter = session.get("count_letter", 0)
        self.description = session.get("description", "")
        self.count_win = session.get("count_win", 0)
        self.count_loss = session.get("count_loss", 0)
        self.image_num = session.get("image_num", "")
        self.try_win = session.get("try_win", 0)
        self.try_loss = session.get("try_loss", 0)
        self.empty_element = session.get("empty_element", "")
        self.used_letters = session.get("used_letters", [])

    def save(self):
        for i in self.data_strings + self.data_ints + self.data_lists:
            session[i] = getattr(self, i)

    def reset(self):
        for i in self.data_strings:
            setattr(self, i, '')
        for j in self.data_ints:
            setattr(self, j, 0)
        for k in self.data_lists:
            setattr(self, k, [])
        self.save()