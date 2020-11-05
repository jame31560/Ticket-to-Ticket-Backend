from .request_models.Auth import Auth_Create_Req
from .response_models.Auth import Auth_Create_Res

Auth_Create_Doc = {
    "tags": ["Auth"],
    "description": "Create a JWT",
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": Auth_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "JWT Token Created",
            "schema": Auth_Create_Res,
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
}
