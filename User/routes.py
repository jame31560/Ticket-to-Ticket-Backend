from app import app
from flask import jsonify
from User.models import User


@app.route("/user/hello", methods=["GET"])
def test():
    a = User()
    return jsonify({"123": "456"}), 200
