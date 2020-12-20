import mongoengine
from mongoengine import document
from mongoengine.fields import *
from mongoengine.document import *
from bson.objectid import ObjectId

class Ticket(EmbeddedDocument):
    oid = ObjectIdField(required=True, default=ObjectId)
    areaId = StringField()
    type = IntField() #1 sale 2 Receive 3 end
    exchange = BooleanField()
    face = BooleanField()
    introduction = StringField()

    def creatTicket(self,area:str,type:int,exchange:bool,face:bool,intro:str):
        self.areaId = area
        self.type = type
        self.exchange = exchange
        self.face = face
        self.introduction = intro

    def get_info(self):
        return{
            "oid":str(self.oid),
            "areaId":self.areaId,
            "tpye":self.type,
            "exchange":self.exchange,
            "face":self.face,
            "intro":self.introduction}