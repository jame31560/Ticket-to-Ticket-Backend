from .request_models.Message import Message_Create_Req
from .response_models.Message import Message_Create_Res

Message_Create_Doc = {
    "tags": ["Sendmsg"],
    "description": "Send message",
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": Message_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "Send message",
            "schema": Message_Create_Res,
            "examples": {
                "application/json": {
                    "msg": "hello world"
                }
            }
        }
    }
}
