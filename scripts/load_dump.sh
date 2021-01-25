#!/bin/sh
exec psql $DATABASE_URL < dump.sql
