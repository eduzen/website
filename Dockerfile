FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH
RUN echo 'alias ll="ls -lh"' >> ~/.bashrc
RUN echo 'alias ll="ls -la"' >> ~/.bashrc

RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
ADD requirements.txt /code
ADD requirements_dev.txt /code
RUN pip install -r requirements_dev.txt
ADD . /code/

WORKDIR /code/website
