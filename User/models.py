from app import db
from passlib.hash import pbkdf2_sha256


class User(db.Document):
    name = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    verify = db.BoolField()
    point = db.IntField()
    role = db.IntField()

    def signup(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = pbkdf2_sha256.encrypt(password)
        self.email = email
        self.verify = False
        self.point = 0
        self.role = 0
        self.save()

    def checkPassword(self, password):
        return True if pbkdf2_sha256.verify(
            password, self.password) else False

    def get_info(self):
        return {
            "id": str(self.mongo_id),
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "point": self.point,
            "role": self.role
        }
