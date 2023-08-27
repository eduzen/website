"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.prod")

from django.core.wsgi import get_wsgi_application  # NOQA

application = get_wsgi_application()
