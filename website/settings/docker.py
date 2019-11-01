"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from .base import show_toolbar
from .base import *  # NOQA


DEBUG = bool(os.environ.get("DEBUG"))
ALLOWED_HOSTS = ["*"]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailhog'  # Your Mailhog Host
EMAIL_PORT = '1025'
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware", "pyinstrument.middleware.ProfilerMiddleware"]  # NOQA
INSTALLED_APPS += ["debug_toolbar"]  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_SERVICE"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN"),
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARN").upper()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} [{asctime}] [{name}.{funcName}:{lineno}]: {message}',
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'style': '{',
        }
    },
    'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'}},
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG'}  # 'catch all' loggers by referencing it with the empty string
    },
}
