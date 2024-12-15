DCO := "docker compose"
RUNDJANGO := "docker compose run --rm web"
EXEC := "docker compose web exec"
DJMANAGE := "docker compose run --rm web python manage.py"

fmt:
  uv run pre-commit run --all-files

logs:
  {{DCO}} logs -f web

run:
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
  {{EXEC}} web bash

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
