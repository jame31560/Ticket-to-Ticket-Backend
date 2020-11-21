from flask_restful_swagger_2 import Schema


class Sendmsg_Create_Res(Schema):
    type = 'object'
    properties = {
        "roomId": {"type": "string"},
        "msg": {"type": "string"},
    }
