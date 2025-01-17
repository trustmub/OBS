FROM python:3.9.6
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
CMD python build_database.py
CMD python create_entries.py
CMD gunicorn --bind 0.0.0.0:8080 obs_app:app
