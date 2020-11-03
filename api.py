from flask_mongoengine import MongoEngine
from config import DOMAIN, JWT_SECRET_KEY, LOCAL, MONGODB_DB, MONGODB_URI, PORT
from controller.authorizer_controller import AuthController
import os

from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': MONGODB_DB,
    'host': MONGODB_URI
}
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

CORS(app, resources={r"*": {"origins": "*", "supports_credentials": True}})

db = MongoEngine(app)
jwt = JWTManager(app)


def is_local():
    return True if LOCAL else False


api = Api(app,
          host=f'localhost:{PORT}' if is_local() else DOMAIN,
          schemes=['http' if is_local() else 'https'],
          base_path='/',
          api_version='0.0.1',
          api_spec_url='/api/swagger')

api.add_resource(AuthController, "/api/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
