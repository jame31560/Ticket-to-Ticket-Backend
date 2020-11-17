from config import DOMAIN, LOCAL,  PORT
from Controller.Auth_Controller import Auth_Controller
from Controller.User_Controller import User, UserList
from flask_restful_swagger_2 import Api, swagger

from app import app


def is_local():
    return True if LOCAL else False


api = Api(app,
          host=f'localhost:{PORT}' if is_local() else DOMAIN,
          schemes=['http' if is_local() else 'https'],
          base_path='/',
          api_version='0.0.1',
          api_spec_url='/api/swagger',
          security_definitions={
              "Bearer": {
                  "type": "apiKey",
                  "name": "Authorization",
                  "in": "header"
              }
          })

api.add_resource(Auth_Controller, "/api/auth")
api.add_resource(UserList, "/api/users")
api.add_resource(User, "/api/users/<string:user_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
