FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements_dev.txt ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        apt-utils \
        libpq-dev \
        postgresql-client \
        httpie && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U pip
RUN pip install -r requirements_dev.txt

WORKDIR /code
ENV PYTHONPATH /code:$PYTHONPATH

# USER uwsgi
EXPOSE 80
COPY . /code/

CMD ["uwsgi", "--ini", "/code/scripts/uwsgi.ini"]
