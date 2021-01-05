import mongoengine
import json
from mongoengine import document
from mongoengine.fields import *
from mongoengine.document import *
from .Mail import Mail
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from Models.Ticket import Ticket


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
    tickets = ListField(EmbeddedDocumentField(Ticket), default=[])
    ticket_verify = BooleanField()
    def signup(self, name: str,
               username: str, password: str, email: str,sex: int,bd: str,
               phone: str,city: str) -> None:
        self.name = name
        self.username = username
        self.password = pbkdf2_sha256.encrypt(password)
        self.email = email
        self.sex = sex
        self.birthday = datetime.strptime((bd), "%Y-%m-%d")
        self.phone = phone
        self.city = city
        self.verify = False
        self.point = 0
        self.ticket_verify = False
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

    def changePhone(self,phone:str):
        try:
            self.phone = phone
            self.save()
            return True
        except:
            return False
    
    def changeSex(self,sex:int):
        try:
            self.sex = sex
            self.save()
        except:
            return False
    
    def changeBirthday(self,bd:str):
        try:
            self.birthday = datetime.strptime((bd), "%Y-%m-%d")
            self.save()
        except:
            return False

    def changeName(self, name: str) -> bool:
        try:
            self.name = name
            self.save()
            return True
        except:
            return False
    
    def changeCity(self, city:str):
        try:
            self.city = city
            self.save()
            return True
        except:
            return False

    def changeEmail(self, email:str):
        try:
            self.email = email
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
            "city":self.city,
            "sex":self.sex,
            "phone":self.phone,
            "birthday":self.birthday.strftime('%Y-%m-%d'),
            "point": self.point,
            "role": self.role
        }

    def verify_email(self) -> None:
        self.token = ""
        self.verify = True
        self.save()

    def add_ticket(self,area:str,type:int,exchange:bool,face:bool,intro:str):
        newTicket = Ticket()
        newTicket.creatTicket(area,type,exchange,face,intro)
        self.tickets.append(newTicket)
        self.save()
    
    def get_tickets(self):
        list = []
        for ticket in self.tickets:
            list.append(ticket.get_info())
        return list 

    def get_ticket_verify(self):
        return self.ticket_verify

    def ticket_verification(self):
        self.ticket_verify = True
        self.save()