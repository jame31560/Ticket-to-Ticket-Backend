from mongoengine.fields import *
from mongoengine.document import *


class Area(EmbeddedDocument):
    name = StringField()
    price = IntField()
    type = IntField()


class Area_Group(EmbeddedDocument):
    name = StringField()
    areas = ListField(EmbeddedDocumentField(Area))


class Event(EmbeddedDocument):
    date = DateTimeField()
    name = StringField()
    venue = StringField()
    area_groups = ListField(EmbeddedDocumentField(Area_Group))
    status = IntField()


class Mark(EmbeddedDocument):
    agree = IntField()
    against = IntField()


class Activity(Document):
    name = StringField()
    website = URLField()
    events = ListField(EmbeddedDocumentField(Event))
    mark = MapField(EmbeddedDocumentField(Mark))
    status = IntField()
