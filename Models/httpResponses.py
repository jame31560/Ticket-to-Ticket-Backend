from flask_restful import abort


class Res():
    status = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        500: "Server Error"
    }

    @classmethod
    def Res200(self, data=None, message=None):
        return {
            "status": "SUCCESS",
            "data": data,
            "message": message or "OK"
        }, 200

    @classmethod
    def Res201(self, data=None, message=None):
        return {
            "status": "SUCCESS",
            "data": data,
            "message": message or "Created"
        }, 201

    @classmethod
    def Res204(self, data=None, message=None):
        return {
            "status": "SUCCESS",
            "data": data,
            "message": message or "No Content"
        }, 204

    @classmethod
    def ResErr(self, code, message=None):
        return {
            "status": "FAILED",
            "data": None,
            "message": message or self.status.get(code, "Error")
        }, code
