import mongoengine as db
from .Message import Message

class Chatroom(db.Document):
    roomname = db.StringField()
    Messagelist = db.EmbeddedDocumentListField(Message, default= [])

    def createChatroom(self,name:str):
        self.roomname = name
        self.Messagelist = []
        self.save()
        
    def appendMessage(self,msg:Message):
        self.Messagelist.append(msg)
        self.save()