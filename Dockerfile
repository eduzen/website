FROM python:3.7-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements_dev.txt ./
RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    libffi-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    musl-dev \
    libpq \
    pcre-dev \
    && pip install --no-cache-dir -r requirements_dev.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Now multistage
FROM python:3.7-alpine

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

RUN apk add --update --no-cache libpq libjpeg-turbo zlib freetype postgresql-client pcre-dev
WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8080
USER uwsgi

COPY . /code/

CMD ["uwsgi", "--ini", "/code/scripts/uwsgi.ini"]
