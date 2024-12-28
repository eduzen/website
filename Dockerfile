FROM python:3.13-slim-bookworm AS production

ARG RELEASE=0.0.0+dev
ENV RELEASE=$RELEASE
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV PATH="/code/.venv/bin:$PATH"
# PYTHONUNBUFFERED non empty value force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE prevents python creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# DJANGO_SETTINGS_MODULE is the settings module to use
ENV DJANGO_SETTINGS_MODULE=website.settings.prod

RUN echo 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gettext \
    curl \
    libpq-dev \
    postgresql-client \
    iputils-ping \
    httpie \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD pyproject.toml uv.lock /code/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . /code

RUN python manage.py collectstatic --no-input
RUN python manage.py compilemessages

EXPOSE 80
CMD ["sh", "/code/scripts/gunicorn_start.sh"]

# DEVELOPMENT
FROM production AS development

ENV DJANGO_SETTINGS_MODULE=website.settings.dev

RUN echo 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras --all-groups --dev

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
