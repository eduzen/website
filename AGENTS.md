# Repository Guidelines

## Project Structure & Module Organization
- Apps: `blog/`, `core/`, `snippets/`, `django_fast/` (each has `models`, `views`, `urls`, `templates`, `static`).
- Project config: `website/` (ASGI/WSGI, `settings/{base,dev,prod,test}.py`).
- Tests: `*/tests/` inside each app; files named `test_*.py`.
- Ops & tooling: `Dockerfile`, `docker-compose*.yml`, `scripts/`, `Makefile`, `justfile`.

## Build, Test, and Development Commands
- Run stack: `just run` or `make start` (Docker Compose detached). View logs: `just logs`.
- Stop/clean: `just stop` or `make down`; hard reset: `just hard-stop`.
- Tests + coverage: `just test` or `make test` (runs `pytest` with coverage). Show report: `make show-coverage`.
- Lint/format: `just fmt` or `make fmt` (ruff, pyupgrade, django-upgrade, djade, typos).
- Type check: `just mypy` or `make mypy`.
- DB: `just makemigrations`, `just migrate`, `make show-migrations`.
- Admin: `just createsuperuser username=alice` or `make superuser`.

## Coding Style & Naming Conventions
- Python 3.13, 4‑space indent, LF endings, max line length 120.
- Tools: Ruff (lint/format), isort (black profile), pyupgrade, django-upgrade, djade, typos.
- Naming: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`.
- Templates live in `app/templates/`; static assets in `app/static/`.

## Testing Guidelines
- Framework: `pytest` with `pytest-django`; tests use `website.settings.test` (configured in `pyproject.toml`).
- Coverage: minimum 80% across `blog`, `core`, `snippets`.
- Place tests in `*/tests/`; name files `test_*.py` with descriptive function names.
- Run locally with `just test`; iterate on a file with `pytest path/to/test_file.py -q`.

## Commit & Pull Request Guidelines
- Commits: imperative mood; prefer Conventional Commits (e.g., `feat:`, `fix:`, `docs:`) with a clear scope.
- Before pushing: run `just fmt`, `just mypy`, and `just test`; ensure Django checks pass.
- PRs: include summary, linked issues, screenshots for UI changes, and migration notes when applicable. CI must be green.

## Security & Configuration Tips
- Do not commit secrets. Use `.env` (seed with `cp .env.sample .env` or `just run` auto-copies).
- Local dev: set `DJANGO_SETTINGS_MODULE=website.settings.dev`. Tests auto-use `website.settings.test`.
- Services run in Docker; open a shell with `just shell` or `make dockershell`.
