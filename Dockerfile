FROM python:3.6-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements_dev.txt ./
RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    libffi-dev \
    python3-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    musl-dev \
    libpq \
    && pip install --no-cache-dir -r requirements_dev.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Now multistage
FROM python:3.6-alpine

RUN apk --no-cache add --virtual libpq

COPY --from=base /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/lib/ /usr/lib/

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8080

COPY . /code/
