from flask import Blueprint 
from flask_restful import Api, Resource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class HelloWorld(Resource):
    def get(self):
        return {'text': 'Hello World'}

api.add_resource(HelloWorld, '/hello')
