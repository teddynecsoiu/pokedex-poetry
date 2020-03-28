import os
basedir = os.path.abspath(os.path.dirname(__file__))

class ClientsConfig(object):
    POKEAPI_URL = 'https://pokeapi.co/api/v2/pokemon/'
    FUNTRANSLATION_URL = 'https://api.funtranslations.com/translate/shakespeare.json'
    FUNTRANSLATION_KEY = ''


class ServerConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-needs-to-be-changed'


class ProductionConfig(ServerConfig):
    DEBUG = False


class StagingConfig(ServerConfig):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(ServerConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(ServerConfig):
    TESTING = True
