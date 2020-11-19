import mongoengine as db
from datetime import datetime

class Message(db.Document):
    to = db.StringField()
    subject = db.StringField()
    content = db.StringField()
    url = db.StringField()
    sendtime = db.DateTimeField()

    def createMessage(self,to: str,sub: str,content: str,url = None):
        self.to = to
        self.subject = sub
        self.content = content
        self.url = url
        self.date = datetime.now()