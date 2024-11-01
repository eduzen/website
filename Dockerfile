FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /code

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.13-slim-bullseye AS production

WORKDIR /code
COPY --from=builder /code /code

# Place executables in the environment at the front of the path
ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 80

ARG RELEASE=0.0.0+dev
ENV RELEASE=$RELEASE

# PYTHONUNBUFFERED non empty value force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE prevents python creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# DJANGO_SETTINGS_MODULE is the settings module to use
ENV DJANGO_SETTINGS_MODULE=website.settings.prod

RUN echo 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

RUN --mount=target=/var/cache/apt,mode=0755,type=cache,sharing=locked \
  apt-get update && apt-get install --no-install-recommends -y \
    gettext \
    curl \
    libpq-dev \
    postgresql-client \
    httpie \
  && rm -rf /var/lib/apt/lists/*

RUN python manage.py collectstatic --no-input
RUN python manage.py compilemessages

CMD ["sh", "/code/scripts/gunicorn_start.sh"]

FROM builder AS development
ENV DJANGO_SETTINGS_MODULE=website.settings.dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras

ENV PATH="/code/.venv/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
