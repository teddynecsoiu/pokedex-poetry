# Pokedex Poetry API

A simple RESTful API that will take any pokemon name and return a Shakespearean description

OpenAPI specification can be found on [Swagger UI](https://app.swaggerhub.com/apis-docs/teddynecsoiu/pokemon/1.0.0#/Pokemon/get_pokemon__pokemon_name_).

## Running the app

#### Running the app locally

Assuming you have `python3` and `pip` already installed on your system.

```bash
# Set up local virtual enviroment
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt

# Set environment config level
export APP_SETTINGS="config.DevelopmentConfig"
export APP_LOGGING="logging.INFO"
export FLASK_ENV=development

# Flask should default to the file but it's better to be specific
export FLASK_APP=app.py

python3 -m flask run
```

#### Running the app in a docker container

```bash
# Build container
docker build -t pokemon .


# Run container
docker run -it -p 5000:5000 \
-e FLASK_ENV=development \
-e APP_LOGGING="logging.INFO" \
-e APP_SETTINGS="config.DevelopmentConfig" \
pokemon
```
