from Swagger_Docs.Chatroom import Chatroom_Create_Doc
from Swagger_Docs.Message import Message_Create_Doc
from jsonschema.exceptions import ValidationError
from mongoengine.errors import ValidationError as Mongo_Validation_Error
from Models.Http_Responses import Res
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import jwt_required,get_jwt_identity
from jsonschema import validate
import traceback
from Models.Chatrooms import Chatrooms
from Models.Message import Message
import json

class Chatroomlist(Resource):
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
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            Chatrooms.object(owner=current_user["username"])
        except Mongo_Validation_Error:
            return Res.ResErr(404, "Room Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

class Chatroom(Resource):
    @jwt_required
    def get(self,room_id):
        try:
            query_room = Chatrooms.objects(id=room_id).first()
            if query_room:
                return Res.Res200(query_room.get_info())
            else:
                return Res.ResErr(404, "Room Not Found")
        except Mongo_Validation_Error:
            return Res.ResErr(404, "Room Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)


class Messagelist(Resource):
    @swagger.doc(Message_Create_Doc)
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            input_json = request.json
            validate(request.json, {
                "properties": {
                    'roomid': {
                        "type": "string",
                    },
                    'msg':{
                        "type": "string"
                    }
                },
                "required": ['roomid','msg']
            })
            new_msg = Message()
            new_msg.createMessage(current_user["username"],input_json["msg"])
            chatroom = Chatrooms.objects(id=input_json["roomid"]).first()
            chatroom.appendMessage(new_msg)
            return Res.Res201(input_json)
        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)