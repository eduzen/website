#!/bin/sh

until pg_isready -h ${DJANGO_DB_SERVICE} -d ${DJANGO_DB_NAME} -U ${DJANGO_DB_USER}; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
>&2 echo "Postgres is up - continuing..."

exec python manage.py runserver 0.0.0.0:8000
