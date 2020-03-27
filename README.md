# Pokedex Poetry API

A simple RESTful API that will take any pokemon name and return a Shakespearean description

## Running the app

Assuming you have `python3` and `pip` already installed on your system.

```bash
# Set up local virtual enviroment
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt

# Flask should default to the file but it's better to be specific
export FLASK_APP=app.py
python3 -m flask run
```
