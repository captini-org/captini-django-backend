#!/usr/bin/env bash

mkdir -p /app/recordings/lessons
# Move contents of /app/lessons to /app/recordings/lessons
mv /app/lessons/ /app/recordings/
mv /app/topics/ /app/recordings/
# mv app/profile.jpg  /app/recordings/user/profile_photos/profile.jpg
if [ $# -gt 0 ]; then
  exec python manage.py "$@"
else
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py makemigrations captini
  python manage.py migrate
  cd prod
  python save.py
  cd ../
  exec python manage.py runserver 0.0.0.0:8000
fi
