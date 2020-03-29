import os
import sys
import logging
from werkzeug.utils import import_string

import redis
from flask import Flask
from flask_restful import Api

from resources import routes

# Optional configuration
if os.environ.get('APP_LOGGING') is not None:
    logging_level = import_string(os.environ.get('APP_LOGGING'))
    logging.basicConfig(level=logging_level)

# Required configuration
redis_client = redis.Redis(host='redis', port=6379) 

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
api = Api(app)

api.add_resource(routes.Pokemon, '/pokemon/<string:pokemon_name>', resource_class_kwargs={'cache': redis_client})
