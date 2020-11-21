from .request_models.Sendmsg import Sendmsg_Create_Req
from .response_models.Sendmsg import Sendmsg_Create_Res

Sendmsg_Create_Doc = {
    "tags": ["Sendmsg"],
    "description": "Send message",
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": Sendmsg_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "Send message",
            "schema": Sendmsg_Create_Res,
            "examples": {
                "application/json": {
                    "msg": "hello world"
                }
            }
        }
    }
}
