import os

from flask import Flask
from resources.routes import api_bp

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.register_blueprint(api_bp)
