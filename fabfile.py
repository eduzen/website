from contextlib import contextmanager

from fabric.api import hosts, prefix, run, sudo
from fabric.context_managers import cd


def restart_gunicorn():
    sudo("supervisorctl restart website")


def restart_nginx():
    sudo("servicectl restart nginx")


def pip_install():
    sudo("pip install -r ../requirements.txt")


def pull():
    run("git pull origin master")


def deploy_static():
    run("./manage.py collectstatic -v0 --noinput")


def make_migrations():
    run("./manage.py makemigrations")


def migrate():
    run("./manage.py migrate")


@contextmanager
def source_virtualenv():
    with prefix("source /home/eduzen/.virtualenvs/website/bin/activate"):
        yield


def purge_pyc():
    sudo(r"find . -name \*.pyc -delete")  # NOQA


@hosts(["eduzen.com.ar"])
def update_repo():
    with cd("eduzen/website"):
        pull()
        purge_pyc()
        with source_virtualenv():
            pip_install()
            make_migrations()
            migrate()
            deploy_static()
            restart_gunicorn()
