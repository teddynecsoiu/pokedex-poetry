import os
import sys
import logging
from werkzeug.utils import import_string

import redis
from flask import Flask
from flask_restful import Api

from resources import routes
from common.util import MockCache

# Check for configuration
config_path = os.environ.get('APP_SETTINGS')
if config_path is None:
    config_path = 'config.ProductionConfig'
logging_path = os.environ.get('APP_LOGGING')
if logging_path is None:
    logging_path = 'logging.ERROR'

# Set logging configuration
logging_level = import_string(logging_path)
logging.basicConfig(level=logging_level)

# Set cache configuration
if import_string(config_path).TESTING is True:
    cache_client = MockCache()
else:
    cache_client = redis.Redis(host='redis', port=6379)

app = Flask(__name__)
app.config.from_object(config_path)
api = Api(app)

api.add_resource(
    routes.Pokemon,
    '/pokemon/<string:pokemon_name>',
    resource_class_kwargs={
        'cache': cache_client})
