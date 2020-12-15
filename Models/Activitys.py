from datetime import datetime
from mongoengine.fields import *
from mongoengine.document import *
from bson.objectid import ObjectId


class Ticket_Type(EmbeddedDocument):
    # oid = ObjectIdField(required=True, default=ObjectId)
    name = StringField()
    price = IntField()


class Area(EmbeddedDocument):
    # oid = ObjectIdField(required=True, default=ObjectId)
    name = StringField()
    ticket_types = ListField(EmbeddedDocumentField(Ticket_Type))
    type = IntField()
    counter = BooleanField()

    def add_ticket_types(self, in_ticket_types):
        ticket_types = []
        for ticket_type in in_ticket_types:
            tmp_area = Ticket_Type(
                name=ticket_type["name"],
                price=ticket_type["price"],
            )
            ticket_types.append(tmp_area)
        self.ticket_types = ticket_types


class Area_Group(EmbeddedDocument):
    # oid = ObjectIdField(required=True, default=ObjectId)
    name = StringField()
    areas = ListField(EmbeddedDocumentField(Area))

    def add_areas(self, in_areas):
        areas = []
        for area in in_areas:
            tmp_area = Area(
                name=area["name"],
                counter=area["counter"],
                type=area["type"],
            )
            tmp_area.add_ticket_types(area["ticket_types"])
            areas.append(tmp_area)
        self.areas = areas


class Event(EmbeddedDocument):
    # oid = ObjectIdField(required=True, default=ObjectId)
    date = DateTimeField()
    name = StringField()
    venue = StringField()
    area_groups = ListField(EmbeddedDocumentField(Area_Group), default=[])
    status = IntField(default=0)
    seating_map_url = URLField()

    def add_area_groups(self, in_area_groups):
        area_groups = []
        for area_group in in_area_groups:
            tmp_area_group = Area_Group(
                name=area_group["name"],
            )
            tmp_area_group.add_areas(area_group["areas"])
            area_groups.append(tmp_area_group)
        self.area_groups = area_groups


class Mark(EmbeddedDocument):
    agree = IntField(default=0)
    against = IntField(default=0)


class Activitys(Document):
    event_type = IntField()
    name = StringField()
    website = URLField()
    events = ListField(EmbeddedDocumentField(Event), default=[])
    mark = EmbeddedDocumentField(Mark, default=Mark())
    status = IntField(default=0)
    artis = ListField(StringField(), default=[])
    create_user = StringField()

    def add_events(self, in_events):
        events = []
        for event in in_events:
            tmp_event = Event(
                date=datetime.strptime(
                    event["date"], "%Y-%m-%dT%H:%M:%SZ"),
                name=event["name"],
                venue=event["venue"],
                seating_map_url=event["seating_map_url"] if "seating_map_url" in event else None,
            )
            tmp_event.add_area_groups(event["area_groups"])
            events.append(tmp_event)
        self.events = events
