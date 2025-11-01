FROM python:3.13-slim-bookworm AS production

ARG RELEASE=0.0.0+dev
ARG BUILD_DATE=unknown
ENV RELEASE=$RELEASE
ENV BUILD_DATE=$BUILD_DATE
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV PATH="/code/.venv/bin:$PATH"
# PYTHONUNBUFFERED non empty value force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE prevents python creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# DJANGO_SETTINGS_MODULE is the settings module to use
ENV DJANGO_SETTINGS_MODULE=website.settings.prod

# Use bash with pipefail for safer pipelines
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN printf '%s\n' 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gettext \
    curl \
    ca-certificates \
    gnupg \
    libpq-dev \
    iputils-ping \
    httpie && \
    install -d /usr/share/keyrings && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgres.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/postgres.gpg] http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y postgresql-client-17 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY pyproject.toml uv.lock /code/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . /code

RUN python manage.py collectstatic --no-input --settings=website.settings.prod && \
    python manage.py compilemessages --settings=website.settings.prod

EXPOSE 80
CMD ["sh", "/code/scripts/gunicorn_start.sh"]

# DEVELOPMENT
FROM production AS development

ENV DJANGO_SETTINGS_MODULE=website.settings.dev

RUN printf '%s\n' 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras --group dev

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:80"]

# E2E TESTING
FROM development AS e2e

# Install additional system dependencies for better browser compatibility
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libnss3-dev \
    libatk-bridge2.0-dev \
    libdrm-dev \
    libxkbcommon-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxrandr-dev \
    libgbm-dev \
    libxss-dev \
    libasound-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras --group dev --group e2e

# Install playwright browsers with dependencies
RUN uv run playwright install --with-deps

CMD ["uv", "run", "pytest", "/code/tests/e2e"]
