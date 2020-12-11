

from Swagger_Docs.User import User_Create_Doc
from jsonschema.exceptions import ValidationError as json_Error
from mongoengine.errors import ValidationError as Mongo_Validation_Error
from Models.Http_Responses import Res
from Models.Users import Users
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate
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
                return Res.ResErr(403)
            admin = Users.objects(id=current_user["id"]).first()
            if admin is None:
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
                        "point": {"type": "integer"},
                        "role": {"type": "integer"},
                    }
                },
                "examples": {
                    "application/json": {
                        "id": "1234567890abcdef12345678",
                        "name": "name",
                        "username": "username",
                        "email": "test@test.com",
                        "point": 100,
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
                        "username": {
                            "type": "string",
                            "minLength": 4,
                            "maxLength": 20
                        },
                        "password": {
                            "type": "string",
                            "minLength": 8
                        },
                        "newPassword": {
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
                        "point": {"type": "integer"},
                        "role": {"type": "integer"},
                    }
                },
                "examples": {
                    "application/json": {
                        "id": "1234567890abcdef12345678",
                        "name": "name",
                        "username": "username",
                        "email": "test@test.com",
                        "point": 100,
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
                        "type": "string",
                    }
                },
                "required": ["password"]
            })
            jwt_user = get_jwt_identity()
            current_user = Users.objects(id=jwt_user["id"]).first()
            if current_user.checkPassword(input_json["password"]):
                try:
                    current_user.changeName(input_json["name"])
                except:
                    pass
                try:
                    if input_json["newPassword"] != input_json["checkPassword"]:
                        return Res.ResErr(400, "PASSWORD NOT EQUAL")
                    current_user.changePassword(input_json["newPassword"])
                except:
                    pass 
                try:
                    current_user.changeCity(input_json["city"])
                except:
                    pass
                try:
                    current_user.changeEmail(input_json["email"])
                except:
                    pass
                return Res.Res200(current_user.get_info())              
            else:
                return Res.ResErr(401, "Bad Password")
        except json_Error as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
