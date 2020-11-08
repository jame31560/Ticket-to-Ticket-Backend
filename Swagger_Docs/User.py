from .request_models.User import User_Create_Req
from .response_models.User import User_Create_Res

User_Create_Doc = {
    "tags": ["User"],
    "description": "Create a User",
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": User_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "User Created",
            "schema": User_Create_Res,
            "examples": {
                "application/json": {
                    "email": "test@test.com",
                    "id": "5f8ddddd86c605f565",
                    "name": "test",
                    "username": "test"
                }
            }
        }
    }
}
