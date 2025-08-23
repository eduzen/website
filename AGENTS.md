# Repository Guidelines

## Project Structure & Module Organization
- Source apps: `blog/`, `core/`, `snippets/`, `django_fast/` (Django apps with `models`, `views`, `urls`, `templates`, `static`).
- Project config: `website/` (ASGI/WSGI, `settings/{base,dev,prod,test}.py`).
- Tests: `*/tests/` inside each app; name files `test_*.py`.
- Ops & tooling: `Dockerfile`, `docker-compose*.yml`, `scripts/`, `Makefile`, `justfile`.

## Build, Test, and Development Commands
- Start stack: `just run` or `make start` (Docker Compose in detached mode; follow logs with `just logs`).
- Stop/clean: `just stop` or `make down`; hard reset: `just hard-stop`.
- Tests + coverage: `just test` or `make test` (runs `pytest` with coverage). Show coverage: `make show-coverage`.
- Lint/format: `just fmt` or `make fmt` (pre-commit: ruff, pyupgrade, djade, typos, etc.).
- Type check: `just mypy` or `make mypy`.
- DB tasks: `just makemigrations`, `just migrate`, `make show-migrations`.
- Admin: `just createsuperuser username=alice` or `make superuser`.

## Coding Style & Naming Conventions
- Python 3.13, 4‑space indent, LF endings, max line length 120.
- Tools: Ruff (lint/format), isort (black profile), pyupgrade, django-upgrade, djade, typos, validate-pyproject.
- Naming: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`.
- Templates in `app/templates/`, static assets in `app/static/`.

## Testing Guidelines
- Framework: `pytest` with `pytest-django`; settings: `website.settings.test` (configured in `pyproject.toml`).
- Coverage: minimum 80% (`tool.coverage.report.fail_under`); sources: `blog`, `core`, `snippets`.
- Place tests in `*/tests/`; use descriptive `test_*.py` and function names.

## Commit & Pull Request Guidelines
- Commits: imperative mood; prefer Conventional Commits (e.g., `feat:`, `fix:`, `docs:`) with a clear scope.
- Before pushing: run `just fmt`, `just mypy`, and `just test` locally.
- PRs: include summary, linked issues, screenshots for UI changes, and migration notes if applicable. CI runs lint, type-check, Django checks, and tests—PRs must be green.

## Security & Configuration Tips
- Do not commit secrets. Use `.env` (seed with `cp .env.sample .env` or `just run` auto-copies).
- Local dev settings: `DJANGO_SETTINGS_MODULE=website.settings.dev`. Tests use `website.settings.test` automatically.
- Database and other services run via Docker; interactive shell: `just shell` or `make dockershell`.
