import time
from typing  import Dict


class User():
    user_in_class: int = 0

    def __init__(self, number):
        self.number = number
        User.add_user(number)

    @staticmethod
    def get_user(number: int):
        User(number)

    @classmethod
    def set_user(cls):
        if cls.user_in_class:
            return cls.user_in_class
        User.del_user_in_class()

    @classmethod
    def add_user(cls, number: int):
        cls.user_in_class = number

    @classmethod
    def del_user_in_class(cls):
        del cls.user_in_class


class User_time():
    time_data = {}

    def __init__(self, number):
        self.number = number
        self.start_time = int(round(time.time(), 0))

        User_time.add_user(number, self)

    @staticmethod
    def get_user(user_id):
        if User_time.time_data.get(user_id) is None:
            User_time(user_id)
            return 'yes'
        else:
            return User_time.count_time(user_id)

    @classmethod
    def count_time(cls, user_id):
        current_time = int(round(time.time(), 0))
        result_time = current_time - cls.time_data[user_id].start_time
        if result_time > 10:
            del cls.time_data[user_id]
            return 'yes'

    @classmethod
    def add_user(cls, user_id: int, user):
        cls.time_data[user_id] = user




