FROM python:3.7

COPY . /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD python3 -m flask run --host=0.0.0.0 --port=5000
