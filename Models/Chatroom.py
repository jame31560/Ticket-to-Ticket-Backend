import mongoengine as db
from .Message import Message

class Chatroom(db.Document):
    Messagelist = db.EmbeddedDocumentListField(Message)

    def createChatroom(self):
        self.Messagelist = []
        
    def appendMessage(self,msg:Message):
        self.Messagelist.append(msg)