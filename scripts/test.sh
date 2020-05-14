#!/bin/sh
export DJANGO_CONFIGURATION=Test
exec python manage.py test
