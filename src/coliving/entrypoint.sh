#!/bin/bash

echo "Make database migrations"
python manage.py makemigrations coliving_site

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
python manage.py runserver

