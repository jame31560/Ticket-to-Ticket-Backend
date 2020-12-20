from .request_models.Ticket import Ticket_Create_Req
from .response_models.Ticket import Ticket_Create_Res

Ticket_Create_Doc = {
    "tags": ["User"],
    "description": "Create a ticket",
    "security": [
            {
                "Bearer": []
            }
        ],
    "parameters": [{
        "name": "body",
        "in": "body",
        "schema": Ticket_Create_Req,
        "required": True
    }],
    "responses": {
        "201": {
            "description": "Ticket Created",
            "schema": Ticket_Create_Res,
            "examples": {
                "application/json": {
                    "areaId": "5fdf11ejehj5j4d6d2ca26851",
                    "type":1,
                    "exchange": "false",
                    "face": "true",
                    "intro": "example ticket"
                }
            }
        }
    }
}
