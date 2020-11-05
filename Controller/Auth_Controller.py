
from Swagger_Docs.Auth import Auth_Create_Doc
from jsonschema.exceptions import ValidationError
from Models.Http_Responses import Res
from Models.Users import Users
from datetime import timedelta
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import create_access_token
from jsonschema import validate
import traceback


class Auth_Controller(Resource):
    @swagger.doc(Auth_Create_Doc)
    def post(self):
        try:
            input_json = request.json
            validate(request.json, {
                "properties": {
                    'username': {
                        "type": "string",
                        "minLength": 4,
                        "maxLength": 20
                    },
                    "password": {
                        "type": "string",
                        "minLength": 8
                    }
                },
                "required": ['username', 'password']
            })
            user = Users.objects(username=input_json["username"]).first()
            if user and user.checkPassword(input_json["password"]):
                if not user.verify:
                    return Res.ResErr(403, "Account unverify")
                expires = timedelta(hours=1)
                result = user.get_info()
                result["token"] = create_access_token(
                    identity={
                        "role": user.role,
                        "id": str(user.id),
                        "username": user.username
                    },
                    expires_delta=expires
                )
                return Res.Res201(result)
            return Res.ResErr(401, "Bad Username/Password")
        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
