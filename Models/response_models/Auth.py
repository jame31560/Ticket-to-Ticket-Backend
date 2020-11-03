from flask_restful_swagger_2 import Schema
from flask_restful_swagger_2 import Schema


class AuthCreateRes(Schema):
    type = 'object'
    properties = {
        "email": {"type": "string"},
        "id": {"type": "string"},
        "name": {"type": "string"},
        "point": {"type": "int"},
        "role": {"type": "int"},
        "token": {"type": "string"},
        "username": {"type": "string"},
    }
