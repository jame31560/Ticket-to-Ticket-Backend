from datetime import datetime
import json
from jsonschema.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.Http_Responses import Res
from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from jsonschema import validate
import traceback
from Models.Activitys import Activitys, Event
from Models.Users import Users


class ActivityList(Resource):
    # def get(self):
    #     try:
    #         result = Activitys.objects().to_json()
    #         return Res.Res200(result)
    #     except:
    #         traceback.print_exc()
    #         return Res.ResErr(500)

    @swagger.doc({
        "tags": ["Activity"],
        "description": "Add an activity",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [{
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "event_type": {
                        "type": "integer"
                    },
                    "artis": {
                        "type":  "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "website": {
                        "type":  "string",
                        "format": "uri"
                    },
                    "events": {
                        "type":  "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "name": {
                                    "type": "string"
                                },
                                "seating_map_url": {
                                    "type": "string",
                                    "format": "uri"
                                },
                                "venue": {
                                    "type": "string"
                                },
                                "area_groups": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string"
                                            },
                                            "areas": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {
                                                            "type": "string"
                                                        },
                                                        "counter": {
                                                            "type": "boolean"
                                                        },
                                                        "type": {
                                                            "type": "integer"
                                                        },
                                                        "ticket_types": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "name": {
                                                                        "type": "string"
                                                                    },
                                                                    "price": {
                                                                        "type": "integer"
                                                                    }
                                                                },
                                                                "required": ["name", "price"]
                                                            }
                                                        }
                                                    },
                                                    "required": ["name", "counter", "type", "ticket_types"]
                                                }
                                            }
                                        },
                                        "required": ["name", "areas"]
                                    }
                                }
                            },
                            "required": ["date", "name", "venue", "area_groups"]
                        }
                    }
                },
                "required": ["name", "artis", "event", "event_type", "website"]
            },
            "required": True
        }],
        "responses": {
            "200": {
                "description": "Activity Created",
                "schema": {},
                "examples": {
                    "application/json": {
                        "status": "SUCCESS",
                        "data": None,
                        "message": "OK"
                    }
                }
            }
        }
    })
    @jwt_required
    def post(self):
        try:
            in_activity = request.json
            validate(in_activity, {
                "properties": {
                    "event_type": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "artis": {
                        "type":  "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "website": {
                        "type":  "string",
                        "format": "uri"
                    },
                    "events": {
                        "type":  "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "name": {
                                    "type": "string"
                                },
                                "seating_map_url": {
                                    "type": "string",
                                    "format": "uri"
                                },
                                "venue": {
                                    "type": "string"
                                },
                                "area_groups": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string"
                                            },
                                            "areas": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {
                                                            "type": "string"
                                                        },
                                                        "counter": {
                                                            "type": "boolean"
                                                        },
                                                        "type": {
                                                            "type": "integer"
                                                        },
                                                        "ticket_types": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "name": {
                                                                        "type": "string"
                                                                    },
                                                                    "price": {
                                                                        "type": "integer"
                                                                    }
                                                                },
                                                                "required": ["name", "price"]
                                                            }
                                                        }
                                                    },
                                                    "required": ["name", "counter", "type", "ticket_types"]
                                                }
                                            }
                                        },
                                        "required": ["name", "areas"]
                                    }
                                }
                            },
                            "required": ["date", "name", "venue", "area_groups"]
                        }
                    }
                },
                "required": ["name", "artis", "events", "event_type"]
            })
            current_user = get_jwt_identity()
            user = Users.objects(id=current_user["id"]).first()
            if user is None:
                return Res.ResErr(403)
            activity = Activitys(
                event_type=in_activity["event_type"],
                name=in_activity["name"],
                website=in_activity["website"] if "website" in in_activity else None,
                artis=in_activity["artis"],
                create_user=current_user["id"]
            )
            activity.add_events(in_activity["events"])
            activity.save()
            return Res.Res200(json.loads(activity.to_json()))
        except ValidationError as e:
            traceback.print_exc()
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)


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
    def get(self):
        try:
            input_json = request.json
            validate(request.json, {
                "properties": {
                    "username": {
                        "type": "string",
                        "minLength": 4,
                        "maxLength": 20
                    },
                    "password": {
                        "type": "string",
                        "minLength": 8
                    }
                },
                "required": ["username", "password"]
            })

        except ValidationError as e:
            return Res.ResErr(400, "Invalid JSON document")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
