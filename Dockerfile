FROM python:3.8-slim-buster
EXPOSE 80

ARG DJANGO_CONFIGURATION=Dev
ARG DJANGO_SECRET_KEY

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup/" \
    VENV_PATH="/opt/pysetup/.venv" \
    DJANGO_CONFIGURATION=${DJANGO_CONFIGURATION} \
    DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN echo 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        postgresql-client \
        httpie && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install

WORKDIR /code

COPY . /code/

RUN python manage.py collectstatic --no-input

CMD ["sh", "/code/scripts/gunicorn_start.sh"]
