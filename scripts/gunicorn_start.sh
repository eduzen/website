#!/bin/sh

# Name of the application
NAME="website"
# Django project directory
DJANGODIR=/code/website
# how many worker processes should Gunicorn spawn
NUM_WORKERS=3
# WSGI module name
DJANGO_WSGI_MODULE=website.wsgi
BIND=0.0.0.0:8080
TIMEOUT=120
LOG_FORMAT="%(h)s %(l)s %(u)s %(t)s [GUNICORN] \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""

until pg_isready -h ${DB_SERVICE} -d ${DB_NAME} -U ${DB_USER}; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
>&2 echo "Postgres is up - continuing...""

echo "### Starting $NAME as `whoami` with $DJANGO_SETTINGS_MODULE"

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --access-logformat="${LOG_FORMAT}" \
  --log-file=-
