from flask_restful_swagger_2 import Schema


class Ticket_Create_Req(Schema):
    type = 'object'
    properties = {
        'areaId': {"type": "string",},
        "type": {"type": "integer",},
        "exchange":{"type":"boolean"},
        "face":{"type":"boolean"},
        "intro":{"type":"string"}
    }
    required = ['areaId', 'type','exchange','face','intro']
