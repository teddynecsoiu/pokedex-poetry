# Pokedex Poetry API

A simple RESTful API that will take any pokemon name and return a Shakespearean description

OpenAPI specification can be found on [Swagger UI](https://app.swaggerhub.com/apis-docs/teddynecsoiu/pokemon/1.0.0#/Pokemon/get_pokemon__pokemon_name_).

## Running the app

#### Running the app in using Docker and Docker Compose

Easiest way by far is to use [Docker Compose](https://docs.docker.com/compose/). 
```bash
# Build container
docker-compose up
```
#### Running the app locally

Since the app uses Redis to cache, you will need to configure the host it in `app.py`.

```python
# app.py 
...
redis_client = redis.Redis(host='localhost', port=6379)
...
```

Assuming you have `python3` and `pip` already installed on your system.

```bash
# Set up local virtual enviroment
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt

# Set optional configuration
export APP_SETTINGS="config.DevelopmentConfig"
export APP_LOGGING="logging.INFO"
export FLASK_ENV=development

# Flask should default to the file but it's better to be specific
export FLASK_APP=app.py

python3 -m flask run
```

## Testing

The test are not exaustive but the run using [Pytest](https://docs.pytest.org/en/latest/).

If you are using Docker Compose, the test are run everytime you start the containers. 

To run the test locally you would first set up the enviroment as mentioned above, then set up the **testing** enviroment.

```bash
export APP_SETTINGS="config.TestingConfig"
python3 -m pytest
```

## TODO

- Handle Rate Limiting headers
- Add asyncio to Requests for concurency 
- Add BDD tests
- Improve configuration
