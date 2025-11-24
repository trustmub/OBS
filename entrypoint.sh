#!/bin/sh
echo "Building database and default entries "

python build_database.py
python create_entries.py

echo "Starting gunicorn"
gunicorn --bind 0.0.0.0:8080 obs_app:app