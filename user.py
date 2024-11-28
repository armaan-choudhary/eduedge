from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id,firstname, lastname, username, password, role_id):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.role_id = role_id