
from Models.response_models.Auth import AuthCreateRes
from Models.request_models.Auth import AuthCreateReq
from Models.httpResponses import Res
from flask_restful import Resource
from flask_restful_swagger_2 import swagger


class AuthController(Resource):
    @swagger.doc({
        'tags': ['Auth'],
        'description': 'Create a JWT',
        'parameters': [{
            'name': 'body',
            'in': 'body',
            'schema': AuthCreateReq,
            'required': True
        }],
        'responses': {
            '201': {
                'description': 'JWT Token Created',
                'schema': AuthCreateRes,
                'examples': {
                    'application/json': {
                        "email": "test@test.com",
                        "id": "5f8ddddd86c605f565",
                        "name": "test",
                        "point": 0,
                        "role": 0,
                        "token": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.eyJpYXQiOjE2MDQ0MDU4NTgsIm5iZiI6MTYadfasdfsdfsdfsafsdfsaTBiYjFiMzktZTc3YjZlY2JhODZjNjA1ZZXJuYW1lIjoi.ooAlRaje4ZP-OXPDYasdfsadfsdaPzcXKeTSlX7fphU",
                        "username": "test"
                    }
                }
            }
        }
    })
    def post(self):
        return Res.Res201()
