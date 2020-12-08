import mongoengine
from mongoengine import document
from mongoengine.fields import *
from mongoengine.document import *
from .Mail import Mail
from passlib.hash import pbkdf2_sha256
from datetime import datetime


class Users(Document):
    name = StringField()
    username = StringField()
    password = StringField()
    email = EmailField()
    verify = BooleanField()
    point = IntField()
    role = IntField()
    token = StringField()
    sex = IntField()
    birthday = DateField()
    phone = StringField()
    city = StringField()

    def signup(self, name: str,
               username: str, password: str, email: str,sex: int,bd: str,
               phone: str,city: str) -> None:
        self.name = name
        self.username = username
        self.password = pbkdf2_sha256.encrypt(password)
        self.email = email
        self.sex = sex
        self.birthday = datetime.strptime((bd), "%Y-%m-%d")
        self.city = city
        self.verify = False
        self.point = 0
        self.role = 0
        self.token = pbkdf2_sha256.encrypt(str(datetime.now()))[
            21:].replace("$", "").replace("/", "")
        self.save()
        mail = Mail()
        mail.send_signup_verify(self.email, self.token, self.name)

    def checkPassword(self, password: str) -> bool:
        return True if pbkdf2_sha256.verify(
            password, self.password) else False

    def changePassword(self, newPassword: str) -> bool:
        try:
            self.password = pbkdf2_sha256.encrypt(newPassword)
            self.save()
            return True
        except:
            return False

    def changeName(self, name: str) -> bool:
        try:
            self.name = name
            self.save()
            return True
        except:
            return False

    def get_info(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "point": self.point,
            "role": self.role
        }

    def verify_email(self) -> None:
        self.token = ""
        self.verify = True
        self.save()
