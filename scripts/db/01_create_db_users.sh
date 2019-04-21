#!/bin/sh
psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';"
