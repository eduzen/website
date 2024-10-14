# syntax = docker/dockerfile:experimental
FROM python:3.13-slim-bullseye as production
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

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -U pip pip-tools wheel

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --no-input
RUN python manage.py compilemessages

CMD ["sh", "/code/scripts/gunicorn_start.sh"]

FROM production as development
ENV DJANGO_SETTINGS_MODULE=website.settings.dev

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements-dev.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
