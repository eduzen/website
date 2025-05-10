#!/bin/sh

# Name of the application
NAME="website"

echo ""
sh /code/scripts/wait_for_db.sh
if [ $? -ne 0 ]; then
  echo "### wait_for_db.sh returned a non-zero exit code, exiting..."
  exit 1
fi

echo ""
echo "### Starting $NAME as $(whoami) with $DJANGO_SETTINGS_MODULE settings ###"
echo "### Using gunicorn.conf.py for dynamic configuration ###"
echo ""

# Start Gunicorn with config file
exec gunicorn --config /code/gunicorn.conf.py
