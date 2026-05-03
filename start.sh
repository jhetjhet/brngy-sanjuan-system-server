#!/bin/bash

# Run makemigrations
echo "Running makemigrations..."
python manage.py makemigrations

# Run migrate
echo "Running migrate..."
python manage.py migrate

# Start Django development server
echo "Starting Django server on 0.0.0.0:8000..."
python manage.py runserver 0.0.0.0:8000
