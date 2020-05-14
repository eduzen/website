ifneq (,$(wildcard ./.env))
    include .env
endif

# Colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
orange=`tput setaf 4`
violet=`tput setaf 5`
lightblue=`tput setaf 6`
reset=`tput sgr0`

DCO=docker-compose
RUNDJANGO=${DCO} run --rm web
UP=${DCO} up${lightblue}
EXEC=docker-compose exec
DJMANAGE=$(RUNDJANGO) python manage.py

start:
	@echo "${UP} -d web db${reset}"
	@docker-compose up -d web db

build:
	@echo "${DCO} build ${lightblue}web${reset}"
	@docker-compose build web

logs:
	@echo "${DCO}${red} logs ${green}-f --tail=50 ${lightblue}web db${reset}"
	@docker-compose logs -f --tail=50 web db

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

only_test:
	docker-compose run --rm web pytest

pep8:
	docker-compose run --rm web flake8

test: pep8 only_test

dockershell:
	docker-compose run --rm web bash

showmigrations:
	$(DJMANAGE) showmigrations

superuser:
	$(DJMANAGE) createsuperuser

migrate:
	@echo "${DCO}${red} run --rm web ${yellow}python manage.py ${lightblue}migrate${reset}"
	@docker-compose run --rm web python manage.py migrate

migrations:
	$(DJMANAGE) makemigrations

shell_plus:
	$(DJMANAGE) shell_plus

shell_plus_sql:
	$(DJMANAGE) shell_plus --print-sql

black:
	docker-compose run --rm --no-deps web black --py36 -l 99 -S .

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
