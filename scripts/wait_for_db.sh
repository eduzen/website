#!/bin/sh

postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(
      dbname="$DJANGO_DB_NAME",
      user="$DJANGO_DB_USER",
      password="$DJANGO_DB_PASS",
      host="$DJANGO_DB_SERVICE",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
>&2 echo "Postgres is up - continuing..."
