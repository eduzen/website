#!/bin/sh

NAME="website"                       # Name of the application
DJANGODIR=/code/website              # Django project directory
NUM_WORKERS=3                        # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=website.wsgi      # WSGI module name
BIND=0.0.0.0:8080
TIMEOUT=120

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$DB_NAME", user="$DB_USER", password="$DB_PASS", host="$DB_SERVICE")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing..."

echo "### Starting $NAME as `whoami` with $DJANGO_SETTINGS_MODULE"

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
