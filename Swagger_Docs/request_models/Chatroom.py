from flask_restful_swagger_2 import Schema


class Chatroom_Create_Req(Schema):
    type = 'object'
    properties = {
        'roomname': {
            "type": "string",
            "maxLength": 20
        }
    }
    required = ['roomname']
