import jsonschema
from flask import jsonify
from app import app


@app.errorhandler(jsonschema.ValidationError)
def onValidationError(e):
    return jsonify(msg="Error request schema"), 400
