from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_restful import Resource, Api

bankapi = Blueprint('bankapi', __name__)

api = Api(bankapi)


@bankapi.route('/api/all/')
def api_all():
    pass


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(bankapi.HelloWorld, '/')
