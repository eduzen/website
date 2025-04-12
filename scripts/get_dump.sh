#!/bin/sh
exec pg_dump -O -x "$DATABASE_URL" > "dump-$(date +%F).sql"
