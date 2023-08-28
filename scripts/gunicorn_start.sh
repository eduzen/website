#!/bin/sh

# Name of the application
NAME="website"
# how many worker processes should Gunicorn spawn
NUM_WORKERS=3
# WSGI module name
DJANGO_WSGI_MODULE=website.wsgi
BIND=0.0.0.0:80
TIMEOUT=120
LOG_FORMAT="[GUNICORN] %(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""

sh /code/scripts/wait_for_db.sh

echo "### Starting $NAME as $(whoami) with $DJANGO_SETTINGS_MODULE and $DJANGO_CONFIGURATION"

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --bind=$BIND \
  --log-level="$LOG_LEVEL" \
  --access-logformat="${LOG_FORMAT}" \
  --log-file=- \
  -k gevent
