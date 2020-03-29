import os
import sys
import logging
from werkzeug.utils import import_string

from flask import Flask
from flask_restful import Api

from resources import routes

if os.environ.get('APP_LOGGING') is None or os.environ.get('APP_SETTINGS') is None:
    print("Configuration missing. Check enviroment and try again!")
    sys.exit()
    

logging_level = import_string(os.environ.get('APP_LOGGING'))
logging.basicConfig(level=logging_level)

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
api = Api(app)

api.add_resource(routes.Pokemon, '/pokemon/<string:pokemon_name>')
