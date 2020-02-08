#!/bin/sh
exec psql postgresql://$DB_USER:$DB_PASS@$DB_SERVICE:$DB_PORT/$DB_NAME  < dump.sql
