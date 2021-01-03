

from Swagger_Docs.User import User_Create_Doc
from Swagger_Docs.Ticket import Ticket_Create_Doc
from jsonschema.exceptions import ValidationError as json_Error
from mongoengine.errors import ValidationError as Mongo_Validation_Error
from Models.Http_Responses import Res
from Models.Users import Users
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate
import json
import traceback
import re


class Validation(Resource):
    @swagger.doc({
        "tags": ["Validation"],
        "description": "verify an User email",
        "parameters": [{
            "name": "body",
            "in": "body",
            "schema": {
                    "type": "object",
                    "properties": {
                        'token': {
                            "type": "string"
                        },
                    },
                "required": ["token"]
            },
            "required": True
        }],
        "responses": {
            "200": {
                "description": "User Verified",
                "schema": {},
                "examples": {
                    "application/json": {
                        "status": "SUCCESS",
                        "data": None,
                        "message": "OK"
                    }
                }
            }
        }
    })
    def put(self):
        try:
            input_json = request.json
            validate(input_json, {
                "properties": {
                    'token': {
                        "type": "string"
                    },
                },
                "required": ['token']
            })
            user = Users.objects(token=input_json["token"]).first()
            if not user:
                return Res.ResErr(404)
            user.verify_email()
            return Res.Res200()
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)


class UserList(Resource):
    @swagger.doc(User_Create_Doc)
    def post(self):
        try:
            input_json = request.json
            validate(input_json, {
                "properties": {
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
                    },
                    "sex":{
                        "type":"integer"
                    },
                    "bd":{
                        "type":"string",
                        "maxLength": 10
                    },
                    "phone":{
                        "type":"string"
                    },
                    "city":{
                        "type":"string"
                    }
                },
                "required": ['name', 'username', 'password',
                             'checkpassword', 'email','sex','bd','phone','city']
            })
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not re.search(regex, input_json["email"]):
                return Res.ResErr(400, "Bad email")
            if input_json["password"] != input_json["checkpassword"]:
                return Res.ResErr(400, "PASSWORD NOT EQUAL")
            if Users.objects(email=input_json["email"]).count() > 0:
                return Res.ResErr(400, "EMAIL USED")
            if Users.objects(username=input_json["username"]).count() > 0:
                return Res.ResErr(400, "USERNAME USED")
            new_user = Users()
            new_user.signup(input_json["name"], input_json["username"],
                            input_json["password"], input_json["email"],
                            input_json["sex"],input_json["bd"],
                            input_json["phone"],input_json["city"])
            return Res.Res201(input_json)
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)


class User(Resource):
    @swagger.doc({
        "tags": ["User"],
        "description": "Delete a User",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [{
            "in": "path",
            "name": "user_id",
            "type": "string",
            "required": True,
            "description": "Numeric ID of the user to delete"
        }],
        "responses": {
            "200": {
                "description": "User Delete",
                "schema": {},
                "examples": {
                    "application/json": {
                        "status": "SUCCESS",
                        "data": None,
                        "message": "OK"
                    }
                }
            }
        }
    })
    @jwt_required
    def delete(self, user_id):
        try:
            current_user = get_jwt_identity()
            if (current_user["role"] != 1):
                print("111")
                return Res.ResErr(403)
            admin = Users.objects(id=current_user["id"]).first()
            if admin is None:
                print("000")
                return Res.ResErr(403)
            user = Users.objects(id=user_id).first()
            if user:
                user.delete()
                return Res.Res200()
            else:
                return Res.ResErr(404, "User Not Found")
        except Mongo_Validation_Error:
            return Res.ResErr(404, "User Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

    @swagger.doc({
        "tags": ["User"],
        "description": "Get a User",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [{
            "in": "path",
            "name": "user_id",
            "type": "string",
            "required": True,
            "description": "Hex ID of the user to get"
        }],
        "responses": {
            "200": {
                "description": "User",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "username": {"type": "string"},
                        "email": {"type": "string",
                                  "format": "email"},
                        "city":{"type":"string"},
                        "sex":{"type":"integer"},
                        "phonne":{"type":"string"},
                        "birthday":{"type":"string"},
                        "point": {"type": "integer"},
                        "role": {"type": "integer"},
                    }
                },
                "examples": {
                    "application/json": {
                        "id": "5fdf01b67cfda035474d83bb",
                        "name": "name",
                        "username": "username",
                        "email": "test@gmail.com",
                        "city": "台中",
                        "sex": 1,
                        "phone": "0987654321",
                        "birthday": "2020-12-31",
                        "point": 0,
                        "role": 0
                    }
                }
            }
        }
    })
    @jwt_required
    def get(self, user_id):
        try:
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user is None:
                return Res.ResErr(403)
            query_user = Users.objects(id=user_id).first()
            if query_user:
                if (str(query_user.id) == str(current_user.id) or
                        current_user.role == 1):
                    return Res.Res200(query_user.get_info())
                else:
                    return Res.ResErr(404)
            else:
                return Res.ResErr(404, "User Not Found")
        except Mongo_Validation_Error:
            return Res.ResErr(404, "User Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

    @swagger.doc({
        "tags": ["User"],
        "description": "Change User information",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [
            {
                "in": "path",
                "name": "user_id",
                "type": "string",
                "required": True,
                "description": "Hex ID of the user to get"
            },
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        'name': {
                            "type": "string",
                            "maxLength": 20
                        },
                        "newPassword": {
                            "type": "string",
                            "minLength": 8
                        },
                        "checkPassword": {
                            "type": "string",
                            "minLength": 8
                        },
                        "sex":{
                            "type":"integer"
                        },
                        "bd":{
                            "type":"string"
                        },
                        "phone":{
                            "type":"string",
                            "maxLength": 10
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "city": {
                            "type": "string",
                        },
                        "password": {
                            "type": "string",
                            "minLength": 8
                        }
                    },
                    "required": ["password"]
                },
                "required": True
            }],
        "responses": {
            "200": {
                "description": "User",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "username": {"type": "string"},
                        "email": {"type": "string",
                                  "format": "email"},
                        "city":{"type":"string"},
                        "sex":{"type":"integer"},
                        "phonne":{"type":"string"},
                        "birthday":{"type":"string"},
                        "point": {"type": "integer"},
                        "role": {"type": "integer"},
                    }
                },
                "examples": {
                    "application/json": {
                        "id": "5fdf01b67cfda035474d83bb",
                        "name": "name",
                        "username": "username",
                        "email": "test@gmail.com",
                        "city": "台中",
                        "sex": 1,
                        "phone": "0987654321",
                        "birthday": "2020-12-31",
                        "point": 0,
                        "role": 0
                    }
                }
            }
        }
    })
    @jwt_required
    def put(self, user_id):
        try:
            input_json = request.json
            validate(input_json, {
                "properties": {
                    'name': {
                        "type": "string",
                        "maxLength": 20
                    },
                    "password": {
                        "type": "string",
                        "minLength": 8
                    },
                    "newPwassword": {
                        "type": "string",
                        "minLength": 8
                    },
                    "checkPassword": {
                        "type": "string",
                        "minLength": 8
                    },
                    "email": {
                        "type": "string",
                        "format": "email"
                    },
                    "city": {
                        "type": "string"
                    },
                    "phone":{
                        "type":"string",
                        "maxLength": 10
                    },
                    "bd":{
                        "type":"string"
                    },
                    "sex":{
                        "type":"integer"
                    }
                },
                "required": ["password"]
            })
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user is None:
                return Res.ResErr(403)
            if current_user.checkPassword(input_json["password"]):
                try:
                    current_user.changeName(input_json["name"])
                except:
                    traceback.print_exc()
                try:
                    if input_json["newPassword"] != input_json["checkPassword"]:
                        return Res.ResErr(400, "PASSWORD NOT EQUAL")
                    current_user.changePassword(input_json["newPassword"])
                except:
                    traceback.print_exc() 
                try:
                    current_user.changeCity(input_json["city"])
                except:
                    traceback.print_exc()
                try:
                    current_user.changeEmail(input_json["email"])
                except:
                    traceback.print_exc()
                try:
                    current_user.changePhone(input_json["phone"])
                except:
                    traceback.print_exc()
                try:
                    current_user.changeBirthday(input_json["bd"])
                except:
                    traceback.print_exc()
                try:
                    current_user.changeSex(input_json["sex"])
                except:
                    traceback.print_exc()
                return Res.Res200(current_user.get_info())              
            else:
                return Res.ResErr(401, "Bad Password")
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

class ticket_verification(Resource):
    @jwt_required
    def get(self):
        try:
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user is None:
                return Res.ResErr(403)
            verification = current_user.get_ticket_verify()
            return Res.Res200(verification)
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
class Ticketlist(Resource):
    @jwt_required
    @swagger.doc(Ticket_Create_Doc)
    def post(self):
        try:
            input_json = request.json
            validate(input_json, {
                "properties": {
                    'areaId': {
                        "type": "string",
                        "maxLength": 20
                    },
                    "type": {
                        "type": "integer",
                    },
                    "exchange": {
                        "type": "boolean",
                    },
                    "face": {
                        "type": "boolean",
                    },
                    "intro": {
                        "type": "string",
                    }
                },
                "required": ['areaId', 'type', 'exchange','face', 'intro']
            })
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user is None:
                return Res.ResErr(403)
            current_user.add_ticket(input_json["areaId"],input_json["type"],
            input_json["exchange"],input_json["face"],input_json["intro"])
            return Res.Res201(input_json)
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

    @swagger.doc({
        "tags": ["User"],
        "description": "Get User Ticketlist",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [{
            "in": "path",
            "name": "user_id",
            "type": "string",
            "required": True,
            "description": "Hex ID of the ticket to get"
        }],
        "responses": {
            "200": {
                "description": "Ticket",
                "schema": {
                    "type": "object",
                    "properties": {
                    }
                },
                "examples": {
                    "application/json": {
    
                    }
                }
            }
        }
    })
    @jwt_required
    def get(self):
        try:
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user is None:
                return Res.ResErr(403)
            tickets = current_user.get_tickets()
            return Res.Res200(tickets)
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
