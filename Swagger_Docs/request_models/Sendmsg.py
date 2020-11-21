from flask_restful_swagger_2 import Schema


class Sendmsg_Create_Req(Schema):
    type = 'object'
    properties = {
        'roomId': {
            "type": "string",
            "maxLength": 20
        },
        "msg":{
            "type": "string",
            "minLength": 4,
            "maxLength": 20
        }
    }
    required = ['roomId','', 'msg']
