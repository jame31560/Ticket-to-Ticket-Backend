from flask_restful_swagger_2 import Schema


class Auth_Create_Res(Schema):
    type = 'object'
    properties = {
        "email": {"type": "string"},
        "id": {"type": "string"},
        "name": {"type": "string"},
        "point": {"type": "integer"},
        "role": {"type": "integer"},
        "token": {"type": "string"},
        "username": {"type": "string"},
    }
