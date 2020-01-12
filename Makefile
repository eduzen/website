ifneq (,$(wildcard ./.env111))
    include .env111
endif
include .env

# Colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
orange=`tput setaf 4`
violet=`tput setaf 5`
lightblue=`tput setaf 6`
reset=`tput sgr0`

DCO=${green}docker-compose${yellow}
RUNDJANGO=${DOC} run --rm ${lightblue}django
UP=${DCO} up${lightblue}
EXEC=docker-compose exec
DJMANAGE=$(RUNDJANGO) python manage.py

start:
	@echo "${UP} -d django postgres${reset}"
	@docker-compose up -d django postgres

build:
	@echo "${DCO} build ${lightblue}django${reset}"
	@docker-compose build django

logs:
	@echo "${DCO}${red} logs ${green}-f --tail=50 ${lightblue}django postgres${reset}"
	@docker-compose logs -f --tail=50 django postgres

pgcli:
	@echo "${green} pgcli ${red}postgres://$(DB_USER):$(DB_PASS)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)${reset}"
	docker-compose run --rm django pgcli postgres://$(DB_USER):$(DB_PASS)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)

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
	$(RUNDJANGO) ash

showmigrations:
	$(DJMANAGE) showmigrations

superuser:
	$(DJMANAGE) createsuperuser

migrate:
	@echo "${DCO}${red} run --rm ${yellow}python manage.py ${lightblue}migrate${reset}"
	@docker-compose run --rm django python manage.py migrate

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
