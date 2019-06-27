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
from flask_cors import CORS
from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors

from src.controller.api_user import ApiUserController
from src.controller.banking_services import BankingServicesController

bank_api = Blueprint("bank_api", __name__)
api = Api(bank_api)
CORS(bank_api)
parser = reqparse.RequestParser()


class Login(Resource):
    # decorators = [cors.make_response('Access-Control-Allow-Origin', '*')]

    # headers.add('Access-Control-Allow-Origin', '*')

    def post(self):
        account = reqparse.request.json["account"]
        pin = reqparse.request.json["pin"]
        device_id = reqparse.request.json["device_id"]
        user_number = reqparse.request.json["user_number"]

        user_obj = ApiUserController(account=account, pin=pin, user_number=user_number, device=device_id)
        if user_obj.verify_account() and user_obj.verify_pin():
            customer = user_obj.customer_details()
            user = user_obj.user_details()
            return jsonify({"response": {"customer": customer, "user": user}})
        return {"response": {"error": "the account does not exist"}}


class Register(Resource):
    def post(self):
        account = reqparse.request.json["account"]
        pin = reqparse.request.json["pin"]
        device_id = reqparse.request.json["device_id"]

        user_obj = ApiUserController(account=account, pin=pin, device=device_id)
        if user_obj.verify_account():
            if not user_obj.verify_registration():
                user_obj.create_mobile_account()
                return jsonify({"response": "successful"})
            return jsonify({"response": "failed"})
        return jsonify({"response": "account does not exist"})


class Services(Resource):

    def post(self):
        account = reqparse.request.json["account"]
        pin = reqparse.request.json["pin"]
        device = reqparse.request.json["device_id"]
        user_number = reqparse.request.json["user_number"]

        user_obj = ApiUserController(account=account, pin=pin, user_number=user_number, device=device)

        if user_obj.verify_account() and user_obj.verify_pin():
            services = BankingServicesController(account).customer_banking_services()
            print("services are {services}")

            return jsonify({
                "response": "success",
                "body": {
                    "account": "serving account",
                    "card_number": "9334 0000 81",
                    "count": 5,
                    "services": services
                }
            })
        else:
            return jsonify({"response": "account does not exist"})


api.add_resource(Login, '/api/v1/login/')
api.add_resource(Register, '/api/v1/login/register/')
api.add_resource(Services, '/api/v1/account/services/')
