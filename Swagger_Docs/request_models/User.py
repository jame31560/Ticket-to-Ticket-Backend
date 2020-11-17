from flask_restful_swagger_2 import Schema


class User_Create_Req(Schema):
    type = 'object'
    properties = {
        'name': {
            "type": "string",
            "maxLength": 20
        },
        "username": {
            "type": "string",
            "minLength": 4,
            "maxLength": 20
        },
        "password": {
            "type": "string",
            "minLength": 8
        },
        "checkpassword": {
            "type": "string",
            "minLength": 8
        },
        "email": {
            "type": "string",
            "format": "email"
        }
    }
    required = ['name', 'username', 'password', 'checkpassword', 'email']
