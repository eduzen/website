DCO := "docker compose"
RUNDJANGO := "docker compose run --rm web"
EXEC := "docker compose web exec uv"
UV := "docker compose run --rm web uv run"
MANAGE := "docker compose run --rm web uv run manage.py"

# Helper recipe
copy-env:
    @if [ ! -f .env ]; then \
        if [ -f .env.sample ]; then \
            cp .env.sample .env; \
        else \
            echo ".env.sample not found, creating empty .env"; \
            touch .env; \
        fi; \
    fi

[group('development')]
run: copy-env
  {{DCO}} up -d
  just logs

[group('development')]
restart:
  {{DCO}} restart web
  just logs

[group('development')]
stop:
  {{DCO}} down

[group('development')]
down:
  just stop

[group('development')]
hard-stop:
  {{DCO}} down -v

[group('development')]
reset:
  {{DCO}} down -v
  {{DCO}} up -d --build

[group('development')]
logs:
  {{DCO}} logs -f web

[group('development')]
shell: copy-env
  {{DCO}} run --rm web bash

[group('development')]
dockershell: shell

[group('development')]
build: copy-env
  {{DCO}} build web

[group('django')]
check:
  {{MANAGE}} check --deploy

[group('django')]
migrate:
  {{MANAGE}} migrate

[group('django')]
makemigrations:
  {{MANAGE}} makemigrations

[group('django')]
createsuperuser username='admin':
  {{MANAGE}} createsuperuser --username "{{username}}" --email "{{username}}@example.com" --noinput

[group('django')]
showurls:
  {{MANAGE}} show_urls

[group('django')]
improve-posts:
  {{MANAGE}} improve_posts

[group('testing')]
test:
  {{UV}} coverage run -m pytest --ignore=tests/e2e

[group('testing')]
coverage:
  {{DCO}} run --rm web uv run coverage run -m pytest --ignore=tests/e2e
  {{DCO}} run --rm web uv run coverage report


# E2E tests using dedicated e2e Docker service
[group('testing')]
e2e *args="tests/e2e":
  {{DCO}} --profile e2e run --rm e2e uv run pytest {{args}}

[group('testing')]
e2e-headed *args="":
  {{DCO}} --profile e2e run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix e2e uv run pytest {{args}} --headed

[group('testing')]
e2e-build:
  {{DCO}} --profile e2e build e2e

[group('code-quality')]
fmt:
  uv run pre-commit run --all-files

[group('code-quality')]
format:
  just fmt

[group('code-quality')]
mypy:
  {{UV}} mypy .
