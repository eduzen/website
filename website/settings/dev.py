import os

from configurations import values

from .base import Base, SelfHostedStorage


class Dev(SelfHostedStorage, Base):
    DEBUG = True
    ALLOWED_HOSTS = values.ListValue(["*"])

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "mailhog"  # Your Mailhog Host
    EMAIL_PORT = "1025"

    DATABASES = values.DatabaseURLValue(conn_max_age=600, ssl_require=False)

    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN"),
    }

    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None
    INTERNAL_IPS = ["127.0.0.1"]
    CORS_ALLOW_ALL_ORIGINS = True

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

    MEDIA_URL = "https://media.eduzen.ar/"

    @property
    def DEBUG_TOOLBAR_CONFIG(self):
        return {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            "debug_toolbar",
            "django_browser_reload",
        ]

    @property
    def MIDDLEWARE(self):
        return (
            ["debug_toolbar.middleware.DebugToolbarMiddleware"]
            + super().MIDDLEWARE
            + ["django_browser_reload.middleware.BrowserReloadMiddleware"]
        )
