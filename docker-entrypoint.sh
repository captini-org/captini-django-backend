#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  exec python manage.py "$@"
else
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py makemigrations captini
  python manage.py migrate

  exec python manage.py runserver 0.0.0.0:8000
fi
