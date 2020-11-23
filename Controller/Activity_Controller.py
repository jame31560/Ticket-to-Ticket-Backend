from jsonschema.exceptions import ValidationError
from flask_jwt_extended import jwt_required
from Models.Http_Responses import Res
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from jsonschema import validate
import traceback


class Activity(Resource):
    @swagger.doc({
        "tags": ["Activity"],
        "description": "Get an Activity",
        "parameters": [{
            "in": "path",
            "name": "activity_id",
            "type": "string",
            "required": True,
            "description": "Hex ID of the activity to get"
        }],
        "responses": {
            "200": {
                "description": "Activity",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "username": {"type": "string"},
                        "email": {"type": "string",
                                  "format": "email"},
                        "point": {"type": "integer"},
                        "role": {"type": "integer"},
                    }
                },
                "examples": {
                    "application/json": {
                        "id": "1234567890abcdef12345678",
                        "name": "Mayday 2020 Life Tour",
                        "website": "https://www.ticket.com",
                        "status": 0,
                        "mark": {
                            "agree": 10,
                            "against": 1
                        },
                        "event": [
                            {
                                "date": "2020/11/23 18:30:00",
                                "name": "Mayday 2020 Life Tour - Taipei",
                                "venue": "Taipei Arena",
                                "status": 0,
                                "area_groups": [
                                    {
                                        "name": "搖滾區",
                                        "areas": [
                                            {
                                                "name": "搖滾A3",
                                                "price": 3880,
                                                "type": 0
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    })
    @jwt_required
    def get(self):
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

        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
