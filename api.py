from config import DOMAIN, LOCAL,  PORT
from Controller.Auth_Controller import Auth_Controller
from Controller.User_Controller import User_Controller
from Controller.Chatroom_Controller import Chatroomlist,Messagelist 
from flask_restful_swagger_2 import Api

from app import app

def is_local():
    return True if LOCAL else False


api = Api(app,
          host=f'localhost:{PORT}' if is_local() else DOMAIN,
          schemes=['http' if is_local() else 'https'],
          base_path='/',
          api_version='0.0.1',
          api_spec_url='/api/swagger')

api.add_resource(Auth_Controller, "/api/auth")
api.add_resource(User_Controller, "/api/user")
api.add_resource(Chatroomlist, "/api/chatroom")
api.add_resource(Messagelist, "/api/message")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
