"""
200 OK
201 Created
202 Accepted

401 Unauthorized (RFC 7235)
403 Forbidden
404 Not Found
408 Request Timeout

500 Internal Server Error
501 Not Implemented
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout


"""

from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse

from src.controller.api_user import ApiUserController

bank_api = Blueprint("bank_api", __name__)
api = Api(bank_api)

parser = reqparse.RequestParser()


class Login(Resource):
    def post(self):
        account = reqparse.request.json["account"]
        pin = reqparse.request.json["pin"]
        user_number = reqparse.request.json["user_number"]

        user_obj = ApiUserController(account=account, pin=pin, user_number=user_number)
        if user_obj.verify_account() and user_obj.verify_pin():
            customer = user_obj.customer_details()
            user = user_obj.user_details()
            return jsonify({"response": {"customer": customer, "user": user}})
        return {"response": {"error": "the account does not exist"}}


class Register(Resource):
    def post(self):
        account = reqparse.request.json["account"]
        pin = reqparse.request.json["pin"]
        user_obj = ApiUserController(account=account, pin=pin)
        if user_obj.verify_account():
            if not user_obj.verify_registration():
                user_obj.create_mobile_account()
                return jsonify({"response": "successful"})
            return jsonify({"response": "failed"})
        return jsonify({"response": "account does not exist"})


api.add_resource(Login, '/api/v1/login/')
api.add_resource(Register, '/api/v1/login/register/')
