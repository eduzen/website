#!/bin/sh
exec pg_dump -O -x postgresql://$DB_USER:$DB_PASS@$DB_SERVICE:$DB_PORT/$DB_NAME  > "dump-$(date +%F).sql"
