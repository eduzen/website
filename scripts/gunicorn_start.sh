#!/bin/sh

NAME="website"                       # Name of the application
DJANGODIR=/code/website              # Django project directory
USER=root                            # the user to run as
GROUP=root                           # the group to run as
NUM_WORKERS=3                        # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=website.wsgi      # WSGI module name
BIND=0.0.0.0:8080
TIMEOUT=120

echo "Starting $NAME as `whoami`"

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
