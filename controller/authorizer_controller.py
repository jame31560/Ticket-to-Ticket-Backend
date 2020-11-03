
from Models.response_models.Auth import AuthCreateRes
from Models.request_models.Auth import AuthCreateReq
from Models.httpResponses import Res
from Models.Users import Users
from datetime import timedelta
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from flask_jwt_extended import create_access_token

from Models.httpResponses import Res


class AuthController(Resource):
    @swagger.doc({
        "tags": ["Auth"],
        "description": "Create a JWT",
        "parameters": [{
            "name": "body",
            "in": "body",
            "schema": AuthCreateReq,
            "required": True
        }],
        "responses": {
            "201": {
                "description": "JWT Token Created",
                "schema": AuthCreateRes,
                "examples": {
                    "application/json": {
                        "email": "test@test.com",
                        "id": "5f8ddddd86c605f565",
                        "name": "test",
                        "point": 0,
                        "role": 0,
                        "token": "json.web.token",
                        "username": "test"
                    }
                }
            }
        }
    })
    def post(self):
        try:
            input_json = request.json
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
        except:
            return Res.ResErr(500)
