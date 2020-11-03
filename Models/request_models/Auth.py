from flask_restful_swagger_2 import Schema


class AuthCreateReq(Schema):
    type = 'object'
    properties = {
        'username': {
            "type": "string",
            "minLength": 4,
            "maxLength": 20
        },
        "password": {
            "type": "string",
            "minLength": 8
        }
    }
    required = ['username', 'password']
