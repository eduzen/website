DCO := "docker compose"
RUNDJANGO := "docker compose run --rm web"
EXEC := "docker compose web exec"
DJMANAGE := "docker compose run --rm web python manage.py"

copy-env:
    @if [ ! -f .env ]; then cp .env.sample .env; fi

fmt:
  uv run pre-commit run --all-files

format:
  just fmt

logs:
  {{DCO}} logs -f web

run: copy-env
  {{DCO}} up -d --build
  just logs

stop:
  {{DCO}} down

hard-stop:
  {{DCO}} down -v

reset:
  {{DCO}} down -v
  {{DCO}} up -d --build

shell: copy-env
  {{EXEC}} web bash

mypy:
  {{RUNDJANGO}} mypy .

check:
  {{DJMANAGE}} check --deploy

migrate:
  {{DJMANAGE}} migrate

makemigrations:
  {{DJMANAGE}} makemigrations

createsuperuser username='admin':
  {{DJMANAGE}} createsuperuser --username {{username}}

coverage:
  {{DCO}} run --rm web uv run coverage run -m pytest
  {{DCO}} run --rm web uv run coverage report

build: copy-env
  {{DCO}} build web

test:
  {{DCO}} run --rm web coverage run -m pytest
