from flask import jsonify, Blueprint, request
from datetime import datetime, timedelta
from User.models import User
from app import app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import traceback

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/verify", methods=["GET"])
@app.validate('auth', 'verify')
def auth_verify():
    """
    User Verify Email
    ---
    tags:
      - Auth
    produces: application/json
    """
    try:
        input_json = request.json
        user = User.query.filter({"token": input_json["token"]}).first()
        if not user:
            return jsonify(msg="ERROR_TOKEN"), 400
        user.verify_email()
        return jsonify(msg="SUCCESS"), 200
    except:
        traceback.print_exc()
        return jsonify(msg="Server Error"), 500


@auth_bp.route("/login", methods=["POST"])
@app.validate('auth', 'login')
def auth_login():
    """
    User Login
    ---
    tags:
      - Auth
    produces: application/json,
    parameters:
    - name: name
      in: path
      type: string
      required: true
    - name: password
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
        input_json = request.json
        user = User.query.filter({"username": input_json["username"]}).first()
        if user and user.checkPassword(input_json["password"]):
            if not user.verify:
                return jsonify(msg="ACCOUNT_NOT_VERIFY"), 403
            expires = timedelta(hours=1)
            result = user.get_info()
            result["token"] = create_access_token(
                identity={
                    "role": user.role,
                    "id": str(user.mongo_id),
                    "username": user.username
                },
                expires_delta=expires
            )
            return jsonify(result), 200
        return jsonify(msg="AUTH_FAIL"), 403
    except:
        traceback.print_exc()
        return jsonify(msg="Server Error"), 500
