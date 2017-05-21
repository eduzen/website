from contextlib import contextmanager

from fabric.api import run
from fabric.api import sudo
from fabric.api import hosts
from fabric.api import prefix
from fabric.context_managers import cd


def restart_gunicorn():
    sudo("supervisorctl restart website")


def restart_nginx():
    sudo('servicectl restart nginx')


def pull():
    run("git pull origin master")


def deploy_static():
    run('./manage.py collectstatic u-v0')


@contextmanager
def source_virtualenv():
    with prefix('source /home/eduzen/.virtualenvs/website/bin/activate'):
        yield


@hosts(['eduzen.com.ar'])
def update_repo():
    with cd('eduzen/website'):
        pull()
        with source_virtualenv():
            deploy_static()
            restart_gunicorn()
