from flask import jsonify, Blueprint, request
from User.models import User,Activity,Event,Ticket
from flask_jwt_extended import jwt_required,get_jwt_identity
from app import app
import traceback

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
        if User.query.filter(User.email == user["email"]).count() > 0:
            return jsonify(msg="EMAIL_USED"), 400
        if User.query.filter(User.username == user["username"]).count() > 0:
            return jsonify(msg="USERNAME_USED"), 400
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

@user_bp.route("/changepassword", methods=["PUT"])
@app.validate('user', 'changePassword')
@jwt_required
def user_changepassword():
    """
    User Change Password
    ---
    tags:
      - User
    produces: application/json
    parameters:
    - name: old_password
      in: path
      type: string
      required: true
    - name: new_password
      in: path
      type: string
      required: true
    - name: check_password
      in: path
      type: string
      required: true
    """
    try:
        current_user = get_jwt_identity()
        inp = request.json
        user = User.query.filter({"username": current_user["username"]}).first()
        if not user:
            return jsonify(msg="ACCOUNT_NOT_FOUND"), 403
        if inp["new_password"] != inp["check_password"]:
            return jsonify(msg="PASSWORD_NOT_EQUAL"), 400
        if not user.checkPassword(inp["old_password"]):
            return jsonify(msg="AUTH_FAIL"), 403
        if user.changePassword(inp["new_password"]):
            return jsonify(msg="SUCCESS"), 200
        else:
            return jsonify(msg="Error"), 500
    except:
        traceback.print_exc()
        return jsonify(msg="Server Error"), 500

@user_bp.route("/changename", methods=["PUT"])
@app.validate('user', 'changeName')
@jwt_required
def user_changename():
    """
    User Change Name
    ---
    tags:
      - User
    produces: application/json
    parameters:
    - name: new_name
      in: path
      type: string
      required: true
    """
    try:
        current_user = get_jwt_identity()
        inp = request.json
        user = User.query.filter({"username": current_user["username"]}).first()
        if user.changeName(inp["new_name"]):
            return jsonify(msg="SUCCESS"), 200
        else:
            return jsonify(msg="Server Error"), 500
    except:
        traceback.print_exc()
        return jsonify(msg="Server Error"), 500

@user_bp.route("/creatactivity", methods=["POST"])
@app.validate('user', 'creatactivity')
def creatActivity():
	"""
    Creat Activity
    ---
    tags:
      - User
    produces: application/json
    parameters:
    - name: new_name
      in: path
      type: string
      required: true
    """
	try:
		inp = request.json
		if Activity.query.filter(Activity.name == inp["name"]).count() > 0:
			return jsonify(msg="Activity Exists"),400
		new_activity = Activity()
		new_activity.creatActivity(inp["name"])
		return jsonify(msg="SUCCESS"), 200
	except:
		traceback.print_exc()
		return jsonify(msg="Server Error"), 500

@user_bp.route("/createvent", methods=["POST"])
@app.validate('user', 'createvent')
def creatEvent():
	try:
		inp = request.json
		activity = Activity.query.filter({"name": inp["activity_name"]}).first()
		# if Event.query.filter(Event.subname == inp["subname"]).count() > 0:
		# 	return jsonify(msg="Event Exists"),400
		new_Event = Event()
		new_Event.creatEvent(inp["subname"],inp["date"],inp["location"])
		activity.addEvent(new_Event)
		return jsonify(msg="SUCCESS"), 200
	except:
		traceback.print_exc()
		return jsonify(msg="Server Error"), 500

@user_bp.route("/creatticket", methods=["POST"])
@app.validate('user', 'creatticket')
@jwt_required
def creatTicket():
	try:
		current_user = get_jwt_identity()
		inp = request.json
		user = User.query.filter({"username": current_user["username"]}).first()
		activity = Activity.query.filter({"name": inp["activity_name"]}).first()
		for eventlist in activity.event:
			if eventlist.subname == inp["subname"]:
				event = eventlist
		new_ticket = Ticket()
		new_ticket.creatTicket(user.name,inp["area"],inp["price"],inp["type"],inp["stuts"])
		event.addTicket(new_ticket)
		return jsonify(msg="SUCCESS"), 200
	except:
		traceback.print_exc()
		return jsonify(msg="Server Error"), 500