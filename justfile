DCO := "docker compose"
RUNDJANGO := "docker compose run --rm web"
EXEC := "docker compose web exec uv"
UV := "docker compose run --rm web uv run"
MANAGE := "docker compose run --rm web uv run manage.py"

copy-env:
    @if [ ! -f .env ]; then cp .env.sample .env; fi

fmt:
  uv run pre-commit run --all-files

format:
  just fmt

logs:
  {{DCO}} logs -f web

run: copy-env
  {{DCO}} up -d
  just logs

restart:
  {{DCO}} restart web
  just logs

stop:
  {{DCO}} down

hard-stop:
  {{DCO}} down -v

reset:
  {{DCO}} down -v
  {{DCO}} up -d --build

shell: copy-env
  {{DCO}} run --rm web bash

dockershell: shell

mypy:
  {{UV}} mypy .

check:
  {{MANAGE}} check --deploy

migrate:
  {{MANAGE}} migrate

makemigrations:
  {{MANAGE}} makemigrations

createsuperuser username='admin':
  {{MANAGE}} createsuperuser --username {{username}}

coverage:
  {{DCO}} run --rm web uv run coverage run -m pytest
  {{DCO}} run --rm web uv run coverage report

build: copy-env
  {{DCO}} build web

test:
  {{UV}} coverage run -m pytest

showurls:
  {{MANAGE}} show_urls

improve-posts:
  {{MANAGE}} improve_posts
