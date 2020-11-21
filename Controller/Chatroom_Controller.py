from Swagger_Docs.Chatroom import Chatroom_Create_Doc
from jsonschema.exceptions import ValidationError
from Models.Http_Responses import Res
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import create_access_token
from jsonschema import validate
import traceback
from Models.Chatroom import Chatroom

class Chatroom_Controller(Resource):
    @swagger.doc(Chatroom_Create_Doc)
    def post(self):
        try:
            input_json = request.json
            validate(request.json, {
                "properties": {
                    'roomname': {
                        "type": "string",
                        "maxLength": 20
                    }
                },
                "required": ['roomname']
            })
            new_chatroom = Chatroom()
            new_chatroom.createChatroom(input_json["roomname"])
            return Res.Res201(input_json)
        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)