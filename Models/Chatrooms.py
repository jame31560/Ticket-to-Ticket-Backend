import mongoengine as db
from .Message import Message

class Chatrooms(db.Document):
    roomname = db.StringField()
    Messagelist = db.EmbeddedDocumentListField(Message, default= [])
    owner = db.ListField()

    def createChatroom(self,name:str,uidA:str,uidB:str):
        self.roomname = name
        self.Messagelist = []
        self.owner = [uidA,uidB]
        self.save()
        
    def appendMessage(self,msg:Message):
        self.Messagelist.append(msg)
        self.save()
    
    def get_info(self) -> dict:
        return {
            "id": str(self.id),
            "roomname": self.roomname,
            "message": self.Messagelist
        }
    