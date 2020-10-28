from app import db
from Models.Mail import Mail
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import traceback


class User(db.Document):
    name = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    verify = db.BoolField()
    point = db.IntField()
    role = db.IntField()
    token = db.StringField()

    def signup(self, name: str,
               username: str, password: str, email: str) -> None:
        self.name = name
        self.username = username
        self.password = pbkdf2_sha256.encrypt(password)
        self.email = email
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
            traceback.print_exc()
            return False

    def changeName(self, name: str) -> bool:
        try:
            self.name = name
            self.save()
            return True
        except:
            traceback.print_exc()
            return False

    def get_info(self) -> dict:
        return {
            "id": str(self.mongo_id),
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

class Ticket(db.Document):
    owner = db.StringField()
    area = db.StringField()
    price = db.IntField()
    type = db.StringField()
    stuts = db.StringField() #For sale, To buy, In transaction,completed
    def creatTicket(self,owner:str,area:str,price:int,type:str,stuts:str):
        self.owner = owner
        self.area = area
        self.price = price
        self.type = type
        self.stuts = stuts
        self.save()

class Event(db.Document):
    date = db.StringField()
    subname = db.StringField()
    location = db.StringField()
    tick = db.ListField(db.DocumentField(Ticket))
    def creatEvent(self,subname:str,date:str,location:str):
        self.subname = subname
        self.date = date
        self.location = location
        self.tick = []
        self.save()

    def addTicket(self,tick:Ticket):
        self.tick.append(tick)
        self.save()
    
class Activity(db.Document):
    name = db.StringField()
    event = db.ListField(db.DocumentField(Event))
  
    def creatActivity(self,name: str):
        self.name = name
        self.event = []
        self.save()
    
    def addEvent(self,event:Event):
        self.event.append(event)
        self.save()
    



