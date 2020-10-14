from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mongoalchemy import MongoAlchemy
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_jsonschema_validator import JSONSchemaValidator

from config import Config, Configdb, ConfigJWT, ConfigSwagger


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Configdb)
app.config.from_object(ConfigJWT)
app.config.from_object(ConfigSwagger)

JSONSchemaValidator(app=app, root="schemas")

jwt = JWTManager()
jwt.init_app(app)

CORS(app)

db = MongoAlchemy(app)

# template = dict(swaggerUiPrefix=LazyString(
#     lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))
# swagger = Swagger(app, template=template)
swagger = Swagger(app)

import handler
import api
