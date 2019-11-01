include .env

RUNDJANGO=docker-compose run --rm django
UP=docker-compose up
EXEC=docker-compose exec
DJMANAGE=$(RUNDJANGO) django python manage.py

help:
	@echo "help  -- print this help"
	@echo "start -- start docker stack"
	@echo "stop  -- stop docker stack"
	@echo "ps    -- show status"
	@echo "build  -- build image"
	@echo "clean -- clean all artifacts"
	@echo "test  -- run tests using docker"
	@echo "dockershell -- run bash inside docker"
	@echo "shell_plus -- run django shell_plus inside docker"
	@echo "bootstrap --build containers, run django migrations, load fixtures and create the a superuser"

build:
	docker-compose build --no-cache web

start:
	docker-compose up -d

up:
	docker-compose up

psql:
	docker-compose exec postgres psql -U postgres

dbshell:
	$(DJMANAGE) dbshell

load-dump:
	docker-compose exec postgres sh psql -U postgres < /docker-entrypoint-initdb.d/dump.sql

collectstatic:
	docker-compose exec django python manage.py collectstatic --no-input --settings=${DJANGO_SETTINGS_MODULE}

stop:
	docker-compose stop

ps:
	docker-compose ps

clean: stop
	docker-compose rm --force -v

only_test:
	docker-compose -f docker-compose.dev.yml run --rm django pytest

pep8:
	docker-compose -f docker-compose.dev.yml run --rm django flake8

test: pep8 only_test

dockershell:
	$(RUNDJANGO) sh

showmigrations:
	$(DJMANAGE) showmigrations

superuser:
	$(DJMANAGE) createsuperuser

migrate:
	$(DJMANAGE) migrate

migrations:
	$(DJMANAGE) makemigrations

shell_plus:
	$(DJMANAGE) shell_plus

shell_plus_sql:
	$(DJMANAGE) shell_plus --print-sql

black:
	docker-compose run --rm --no-deps django black --py36 -l 99 -S .

clean-python: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

hard-clean-python: clean-build clean-pyc

.PHONY: help start stop ps clean test dockershell shell_plus only_test pep8

