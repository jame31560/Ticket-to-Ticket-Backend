from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mongoalchemy import MongoAlchemy

from config import Config, Configdb, ConfigJWT


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Configdb)
app.config.from_object(ConfigJWT)

jwt = JWTManager()
jwt.init_app(app)

CORS(app)

db = MongoAlchemy(app)
from User import routes

# from .api import bp_api

# app.register_blueprint(bp_api, url_prefix="/api")
