#!/bin/sh

postgres_ready() {
python << END
import sys
import psycopg

try:
    conn = psycopg.connect("$DATABASE_URL")
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
>&2 echo "Postgres is up - continuing..."
