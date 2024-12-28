#!/bin/sh

# Name of the application
NAME="website"
# how many worker processes should Gunicorn spawn
NUM_WORKERS=3
# WSGI module name
DJANGO_WSGI_MODULE=website.wsgi
BIND=0.0.0.0:80
TIMEOUT=120
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_FORMAT="[GUNICORN] %(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""

echo ""
sh /code/scripts/wait_for_db.sh
if [ $? -ne 0 ]; then
  echo "### wait_for_db.sh returned a non-zero exit code, exiting..."
  exit 1
fi

echo ""
echo "### Starting $NAME as $(whoami) with $DJANGO_SETTINGS_MODULE settings ###"
echo "### Listening on $BIND, log level $LOG_LEVEL, worker class gevent...  ###"
echo ""

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
