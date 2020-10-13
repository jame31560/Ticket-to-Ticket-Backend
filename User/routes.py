from flask import jsonify, Blueprint, request
from User.models import User
from app import app

user_bp = Blueprint("user", __name__)


@user_bp.route("/signup", methods=["POST"])
@app.validate('user', 'signup')
def user_signup():
    """
    User Sign Up
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: name
      in: path
      type: string
      required: true
    - name: node_id
      in: path
      type: string
      required: true
    responses:
      401:
        description: Unauthorized error
      200:
        description: Retrieve node list
        example:
          {'code':1,'message':注册成功}
    """
    try:
        user = request.json
        if user["password"] != user["check_password"]:
            return jsonify(msg="password not equal"), 400
        new_user = User()
        new_user.signup(user["name"], user["username"],
                        user["password"], user["email"])
        return jsonify(
            id=str(new_user.mongo_id),
            name=new_user.name,
            username=new_user.username,
            email=new_user.email), 200
    except:
        return jsonify(msg="Server Error"), 500
