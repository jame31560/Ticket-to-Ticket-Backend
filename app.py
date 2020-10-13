from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mongoalchemy import MongoAlchemy
from flasgger import Swagger
from flask_jsonschema_validator import JSONSchemaValidator

from config import Config, Configdb, ConfigJWT


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Configdb)
app.config.from_object(ConfigJWT)

JSONSchemaValidator(app=app, root="schemas")

jwt = JWTManager()
jwt.init_app(app)

CORS(app)

db = MongoAlchemy(app)

swagger = Swagger(app)

import handler
import api
