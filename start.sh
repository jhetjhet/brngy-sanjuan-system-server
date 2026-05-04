#!/bin/bash
set -e  # Exit immediately on error

# Run makemigrations
echo "Running makemigrations..."
python manage.py makemigrations

# Run migrate
echo "Running migrate..."
python manage.py migrate --noinput

exec "$@" # Execute the command passed as arguments to the container