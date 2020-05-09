#!/bin/bash


echo "Setting: ${DJANGO_SETTINGS_MODULE}"

# Migrate DB
echo "Migrate DB"
python manage.py migrate

echo "Run server..."
gunicorn iwantmasterdrf.wsgi --bind 0.0.0.0:8000 --workers 2 --threads 2
