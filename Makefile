ifneq (,$(wildcard ./.env))
    include .env
endif

DCO=docker-compose
RUNDJANGO=${DCO} run --rm web
UP=${DCO} up${lightblue}
EXEC=docker-compose exec
DJMANAGE=$(RUNDJANGO) python manage.py

fmt:
	pre-commit run -a

mypy:
	mypy .

start:
	docker-compose up -d

build:
	docker-compose build web

logs:
	docker-compose logs -f --tail=50 web

pgcli:
	docker-compose run --rm web pgcli ${DATABASE_URL}

psql:
	docker-compose run --rm python manage.py dbshell

dbshell:
	$(DJMANAGE) dbshell

collectstatic:
	docker-compose exec web python manage.py collectstatic --no-input --settings=${DJANGO_SETTINGS_MODULE}

stop:
	docker-compose stop

ps:
	docker-compose ps

clean: stop
	docker-compose rm --force -v

test:
	docker-compose run --rm web sh scripts/test.sh

dockershell:
	docker-compose run --rm web bash

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

clear_cache:
	$(DJMANAGE) clear_cache

show_urls:
	docker-compose run --rm web python manage.py show_urls

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

help:
	@echo "help  -- print this help"
	@echo "start -- start docker stack"
	@echo "stop  -- stop docker stack"
	@echo "ps    -- show status"
	@echo "build  -- build image"
	@echo "clean -- clean all artifacts"
	@echo "test  -- run tests using docker"
	@echo "dockershell -- run bash inside docker"
	@echo "shell_plus -- run web shell_plus inside docker"
	@echo "bootstrap --build containers, run web migrations, load fixtures and create the a superuser"
