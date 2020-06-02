#!/bin/sh

sh /code/scripts/wait_for_db.sh

exec python manage.py runserver 0.0.0.0:8000
