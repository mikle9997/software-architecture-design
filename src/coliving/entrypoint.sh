#!/bin/bash

action=${1:-"run"}
cmd=""

if   [[ $action == "run" ]]; then
	cmd="runserver 0.0.0.0:8000"
elif [[ $action == "test" ]]; then
	cmd="test endpoints"
fi

echo "Make database migrations"
python manage.py makemigrations coliving_site

echo "Apply database migrations"
python manage.py migrate

if   [[ $action == "run" ]]; then
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
fi

echo "Starting server"
python manage.py $cmd

