from flask_restful_swagger_2 import Schema
from flask_restful_swagger_2 import Schema


class User_Create_Res(Schema):
    type = 'object'
    properties = {
        "email": {"type": "string"},
        "id": {"type": "string"},
        "name": {"type": "string"},
        "username": {"type": "string"},
    }
