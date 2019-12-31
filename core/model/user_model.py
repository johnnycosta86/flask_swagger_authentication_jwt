from flask import request, url_for
from requests import post


class UserModel:
    user_id = None
    login = None
    password = None
    email = None
    active = None

    def __init__(self, login, password, email, active):
        self.login = login
        self.password = password
        self.email = email
        self.active = active

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'active': self.active
        }

    @classmethod
    def find_user(cls, user_id):
        for user_found in users:
            if user_found.user_id == user_id:
                return user_found
        return False

    @classmethod
    def find_by_email(cls, email):
        for user_found in users:
            if user_found.email == email:
                return user_found
        return False

    @classmethod
    def find_by_login(cls, login):
        for user_found in users:
            if user_found.login == login:
                return user_found
        return False

    @classmethod
    def find_all(cls):
        return users

    def save_user(self):

        next_id = UserModel.find_last_id()

        self.user_id = next_id

        users.append(self)

    def delete_user(self):
        users.remove(self)
        return self

    @classmethod
    def find_last_id(cls):
        next_id = 0

        for user_found in users:
            if user_found.user_id >= next_id:
                next_id = user_found.user_id + 1
        return next_id


admin = UserModel('admin', 'admin', 'admin@email.com', True)
admin.user_id = 1

user = UserModel('user', 'user', 'user@email.com', True)
user.user_id = 2

users = [admin, user]
