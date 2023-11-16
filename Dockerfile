FROM python:3.9.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "obs_app.py"]
CMD ["python", "build_database.py"]
CMD ["python", "create_entries.py"]