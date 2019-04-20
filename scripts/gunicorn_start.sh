#!/bin/sh

NAME="website"                       # Name of the application
DJANGODIR=/code/website              # Django project directory
SOCKFILE=/code/website/website.sock  # we will communicte using this unix socket
USER=root                            # the user to run as
GROUP=root                           # the group to run as
NUM_WORKERS=3                        # how many worker processes should Gunicorn spawn
TIMEOUT=120
DJANGO_SETTINGS_MODULE=website.settings.production  # which settings file should Django use
DJANGO_WSGI_MODULE=website.wsgi                     # WSGI module name
BIND=0.0.0.0:8000

echo "Starting $NAME as `whoami`"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --bind=$BIND \
  --log-level=INFO \
  --log-file=-
