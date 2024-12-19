DCO := "docker compose"
RUNDJANGO := "docker compose run --rm web"
EXEC := "docker compose web exec"
DJMANAGE := "docker compose run --rm web python manage.py"

copy-env:
    @if [ ! -f .env ]; then cp .env.sample .env; fi

fmt:
  uv run pre-commit run --all-files

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

shell:
  {{DCO}} run --rm web bash

mypy:
  {{RUNDJANGO}} mypy .

check:
  {{DJMANAGE}} check --deploy

migrate:
  {{DJMANAGE}} migrate

make-migrations:
  {{DJMANAGE}} makemigrations

createsuperuser:
  {{DJMANAGE}} createsuperuser
