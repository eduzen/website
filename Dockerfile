FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN echo 'export PS1="\[\e[36m\]eduzenshell>\[\e[m\] "' >> /root/.bashrc

COPY requirements.txt requirements_dev.txt ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
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

RUN python manage.py collectstatic --no-input --settings=website.settings --configuration=Dokku

CMD ["uwsgi", "--ini", "/code/scripts/uwsgi.ini"]
