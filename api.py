from flask import jsonify, Blueprint
from app import app

from User.routes import user_bp
from Auth.routes import auth_bp


api_bp = Blueprint("api", __name__)


@api_bp.route("/heartbeat", methods=["GET"])
def heartbeat():
    """
    Check Backend status
    ---
    tags:
      - Other
    responses:
      500:
        description: Backend dead
      200:
        description: Backend alive
        content:
          application/json:
            example: {"msg": "Hi There!"}
    """
    try:
        return jsonify(msg="Hi There!"), 200
    except:
        return jsonify(msg="ERROR"), 500


app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(api_bp, url_prefix="/api")
