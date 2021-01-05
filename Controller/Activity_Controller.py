from datetime import datetime
import json
import re
from jsonschema.exceptions import ValidationError
from mongoengine.errors import ValidationError as Mongo_Validation_Error
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
    @swagger.doc({
        "tags": ["Activity"],
        "description": "Get Activitys",
        "parameters": [{
            "in": "query",
            "name": "keyword",
            "type": "string",
            "required": False,
            "description": "Filter activity string"
        }, {
            "in": "query",
            "name": "page",
            "type": "integer",
            "required": False,
            "description": "pages"
        }, {
            "in": "query",
            "name": "limit",
            "type": "integer",
            "required": False,
            "description": "items per page"
        }],
        "responses": {
            "200": {
                "description": "Activitys",
                "schema": {},
                "examples": {
                    "application/json": {
                        "id": "1234567890abcdef12345678",
                        "name": "name",
                        "username": "username",
                        "email": "test@test.com",
                        "point": 100,
                        "role": 0
                    }
                }
            }
        }
    })
    def get(self):
        try:
            args = request.args
            print(args)

            if "keyword" in args:
                regex = re.compile(".*" + args["keyword"] + ".*")
                result = Activitys.objects(name=regex)
            else:
                result = Activitys.objects()
            limit = int(args["limit"]) if ("limit" in args and
                                           0 < int(args["limit"]) <= 50) else 50
            page = int(args["page"]) if (
                "page" in args and int(args["page"]) > 0) else 1
            offset = (page - 1) * limit
            result = result.skip(offset).limit(limit)
            return Res.Res200(json.loads(result.to_json()))
        except:
            traceback.print_exc()
            return Res.ResErr(500)

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
                    "img_url": {
                        "type": "string",
                        "format": "uri"
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
                        "data": {
                            "_id": {
                                "$oid": "5fd87ceaab5c2bb24eda40e8"
                            },
                            "event_type": 0,
                            "name": "五月天 [ 好好好想見到你 ] Mayday Fly to 2021 演唱會",
                            "img_url": "https://static.tixcraft.com/images/activity/20_MAYDAY_8987933be02c14b4d8048f5fb91c1fab.jpg",
                            "website": "https://tixcraft.com/activity/detail/20_MAYDAY",
                            "events": [
                                    {
                                        "_id": {
                                            "$oid": "5fd87ceaab5c2bb24eda40dd"
                                        },
                                        "date": {
                                            "$date": 1608921000000
                                        },
                                        "name": "五月天 [ 好好好想見到你 ] Mayday Fly to 2021 演唱會",
                                        "venue": "桃園國際棒球場",
                                        "area_groups": [
                                            {
                                                "_id": {
                                                    "$oid": "5fd87ceaab5c2bb24eda40de"
                                                },
                                                "name": "好好搖滾區",
                                                "areas": [
                                                    {
                                                        "_id": {
                                                            "$oid": "5fd87ceaab5c2bb24eda40df"
                                                        },
                                                        "name": "好好搖滾區 A1",
                                                        "ticket_types": [
                                                            {
                                                                "_id": {
                                                                    "$oid": "5fd87ceaab5c2bb24eda40e0"
                                                                },
                                                                "name": "全票",
                                                                "price": 3880
                                                            }
                                                        ],
                                                        "type": 0,
                                                        "counter": True
                                                    },
                                                    {
                                                        "_id": {
                                                            "$oid": "5fd87ceaab5c2bb24eda40e1"
                                                        },
                                                        "name": "好好搖滾區 A2",
                                                        "ticket_types": [
                                                            {
                                                                "_id": {
                                                                    "$oid": "5fd87ceaab5c2bb24eda40e2"
                                                                },
                                                                "name": "全票",
                                                                "price": 3880
                                                            }
                                                        ],
                                                        "type": 0,
                                                        "counter": True
                                                    }
                                                ]
                                            },
                                            {
                                                "_id": {
                                                    "$oid": "5fd87ceaab5c2bb24eda40e3"
                                                },
                                                "name": "西下看台區",
                                                "areas": [
                                                    {
                                                        "_id": {
                                                            "$oid": "5fd87ceaab5c2bb24eda40e4"
                                                        },
                                                        "name": "西下A",
                                                        "ticket_types": [
                                                            {
                                                                "_id": {
                                                                    "$oid": "5fd87ceaab5c2bb24eda40e5"
                                                                },
                                                                "name": "全票",
                                                                "price": 2880
                                                            }
                                                        ],
                                                        "type": 0,
                                                        "counter": True
                                                    },
                                                    {
                                                        "_id": {
                                                            "$oid": "5fd87ceaab5c2bb24eda40e6"
                                                        },
                                                        "name": "西下F(視線遮蔽區)",
                                                        "ticket_types": [
                                                            {
                                                                "_id": {
                                                                    "$oid": "5fd87ceaab5c2bb24eda40e7"
                                                                },
                                                                "name": "全票",
                                                                "price": 1880
                                                            }
                                                        ],
                                                        "type": 0,
                                                        "counter": True
                                                    }
                                                ]
                                            }
                                        ],
                                        "status": 0,
                                        "seating_map_url": "https://static.tixcraft.com/images/activity/field/20_MAYDAY_f8eddcfc8d9bfa9f1cecd7fc93e13eda.png"
                                    }
                            ],
                            "mark": {
                                "agree": 0,
                                "against": 0
                            },
                            "status": 0,
                            "artis": [
                                "Mayday 五月天"
                            ],
                            "create_user": "5fb412c16df3eeb655736d5b"
                        },
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
                    "img_url": {
                        "type": "string",
                        "format": "uri"
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
                img_url=in_activity["img_url"],
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
            "name": "id",
            "type": "string",
            "required": True,
            "description": "Hex ID of the activity to get"
        }],
        "responses": {
            "200": {
                "description": "Activity",
                "schema": {},
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
    def get(self, id):
        try:
            result = Activitys.objects(id=id).first()
            if result is None:
                return Res.ResErr(404)
            return Res.Res200(json.loads(result.to_json()))
        except Mongo_Validation_Error:
            return Res.ResErr(404, "User Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)

    @swagger.doc({
        "tags": ["Activity"],
        "description": "Delete an Activity",
        "security": [
            {
                "Bearer": []
            }
        ],
        "parameters": [{
            "in": "path",
            "name": "id",
            "type": "string",
            "required": True,
            "description": "Numeric ID of the activity to delete"
        }],
        "responses": {
            "200": {
                "description": "Activity Delete",
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
    def delete(self, id):
        try:
            current_user = get_jwt_identity()
            if (current_user["role"] != 1):
                return Res.ResErr(403)
            admin = Users.objects(id=current_user["id"]).first()
            if admin is None:
                return Res.ResErr(403)
            activity = Activitys.objects(id=id).first()
            if activity:
                activity.delete()
                return Res.Res200()
            else:
                return Res.ResErr(404, "Activity Not Found")
            return Res.Res200()
        except Mongo_Validation_Error:
            return Res.ResErr(404, "Activity Not Found")
        except:
            traceback.print_exc()
            return Res.ResErr(500)
