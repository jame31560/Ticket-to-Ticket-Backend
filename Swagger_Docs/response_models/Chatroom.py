from flask_restful_swagger_2 import Schema


class Chatroom_Create_Res(Schema):
    type = 'object'
    properties = {
        "roomname": {"type": "string"},
    }
