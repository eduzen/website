#!/bin/sh

until pg_isready -h ${DB_SERVICE} -d ${DB_NAME} -U ${DB_USER}; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
>&2 echo "Postgres is up - continuing..."

exec python manage.py runserver_plus 0.0.0.0:8000
