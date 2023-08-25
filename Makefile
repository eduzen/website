ifneq (,$(wildcard ./.env))
    include .env
endif

DCO=docker compose
RUNDJANGO=${DCO} run --rm web
UP=${DCO} up${lightblue}
EXEC=${DCO} exec
DJMANAGE=$(RUNDJANGO) python manage.py


compile-requirements-prod:
	${RUNDJANGO} pip-compile pyproject.toml -o requirements.txt

compile-requirements-dev:
	${RUNDJANGO} pip-compile --all-extras pyproject.toml -o requirements-dev.txt

update-requirements-prod:
	${RUNDJANGO} pip-compile --upgrade pyproject.toml -o requirements.txt

update-requirements-dev:
	${RUNDJANGO} pip-compile --upgrade --all-extras pyproject.toml -o requirements-dev.txt

compile-requirements: compile-requirements-prod compile-requirements-dev

update-requirements: update-requirements-prod update-requirements-dev

fmt:
	pre-commit run -a

remove:
	${DCO} down -v --remove-orphans

down:
	${DCO} down

mypy:
	${RUNDJANGO} mypy .

start:
	${DCO} up -d

build:
	${DCO} build web

restart:
	${DCO} restart web

logs:
	${DCO} logs -f --tail=50 web

pgcli:
	${DCO} run --rm web pgcli ${DATABASE_URL}

psql:
	${DCO} run --rm python manage.py dbshell

dbshell:
	$(DJMANAGE) dbshell

messages:
	$(DJMANAGE) makemessages --locale=es

compile-messages:
	$(DJMANAGE) compilemessages

collectstatic:
	${DCO} exec web python manage.py collectstatic --no-input --settings=${DJANGO_SETTINGS_MODULE}

stop:
	${DCO} stop

ps:
	${DCO} ps

clean: stop
	${DCO} rm --force -v

test:
	${DCO} run --rm web coverage run -m pytest

check:
	${DCO} run --rm web python manage.py check

dockershell:
	${DCO} run --rm web bash

show-migrations:
	$(DJMANAGE) showmigrations

superuser:
	$(DJMANAGE) createsuperuser

migrate:
	$(DJMANAGE) migrate

migrations:
	$(DJMANAGE) makemigrations

shell-plus:
	$(DJMANAGE) shell_plus

shell-plus-sql:
	$(DJMANAGE) shell_plus --print-sql

clear-cache:
	$(DJMANAGE) clear_cache

show-urls:
	${DCO} run --rm web python manage.py show_urls

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
