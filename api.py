from controller.authorizer_controller import AuthController
import os

from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from config import *

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*", "supports_credentials": True}})


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
