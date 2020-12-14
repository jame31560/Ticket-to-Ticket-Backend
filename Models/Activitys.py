from mongoengine.fields import *
from mongoengine.document import *


class Ticket_Type(EmbeddedDocument):
    name = StringField()
    price = IntField()


class Area(EmbeddedDocument):
    name = StringField()
    ticket_type = ListField(EmbeddedDocumentField(Ticket_Type))
    type = IntField()
    counter = BooleanField()


class Area_Group(EmbeddedDocument):
    name = StringField()
    areas = ListField(EmbeddedDocumentField(Area))


class Event(EmbeddedDocument):
    date = DateTimeField()
    name = StringField()
    venue = StringField()
    area_groups = ListField(EmbeddedDocumentField(Area_Group))
    status = IntField()
    seating_map_url = StringField()


class Mark(EmbeddedDocument):
    agree = IntField()
    against = IntField()


class Activitys(Document):
    event_type = IntField()
    name = StringField()
    website = URLField()
    events = ListField(EmbeddedDocumentField(Event))
    mark = MapField(EmbeddedDocumentField(Mark))
    status = IntField()
    artis = ListField(StringField())
