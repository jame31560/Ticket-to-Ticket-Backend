
from Swagger_Docs.User import User_Create_Doc
from jsonschema.exceptions import ValidationError
from Models.Http_Responses import Res
from Models.Users import Users
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from jsonschema import validate
import traceback
import re


class User_Controller(Resource):
    @swagger.doc(User_Create_Doc)
    def post(self):
        try:
            input_json = request.json
            validate(request.json, {
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
                    }
                },
                "required": ['name', 'username', 'password', 'checkpassword', 'email']
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
                            input_json["password"], input_json["email"])
            return Res.Res201(input_json)
        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
