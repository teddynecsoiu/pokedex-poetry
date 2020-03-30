FROM python:3.7

COPY . /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

ENV APP_SETTINGS config.TestingConfig

RUN python3 -m pytest

ENV APP_SETTINGS config.DevelopmentConfig

CMD python3 -m flask run --host=0.0.0.0 --port=5000
