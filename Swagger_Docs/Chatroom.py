from .request_models.Chatroom import Chatroom_Create_Req
from .response_models.Chatroom import Chatroom_Create_Res

Chatroom_Create_Doc = {
    "tags": ["Chatroom"],
    "description": "Create a Chatroom",
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": Chatroom_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "User Created",
            "schema": Chatroom_Create_Res,
            "examples": {
                "application/json": {
                    "roomname": "Jamse's Chatroom"
                }
            }
        }
    }
}
