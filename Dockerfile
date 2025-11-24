FROM python:3.9.6
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get install -y default-mysql-client

COPY . /app
#CMD gunicorn --bind 0.0.0.0:8080 obs_app:app
