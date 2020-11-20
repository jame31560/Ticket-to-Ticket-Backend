import mongoengine as db
from datetime import datetime

class Message(db.Document):
    sender = db.StringField()
    content = db.StringField()
    sendtime = db.DateTimeField()

    def createMessage(self,sender: str,content: str):
        self.sender = sender
        self.content = content
        self.date = datetime.now()