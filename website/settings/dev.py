import logfire
from decouple import config

from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

logfire.configure(send_to_logfire="if-token-present", environment="local")
logfire.instrument_django()
logfire.instrument_psycopg()

ALLOWED_HOSTS = ["*"]

SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
INTERNAL_IPS = ["127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS = True

MEDIA_URL = "https://media.eduzen.ar/"

# Local filesystem paths for dbbackup in development
DBBACKUP_STORAGE = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
    "LOCATION": "/code/backup/",
}

# Use a safe template that does not require database_name
DBBACKUP_FILENAME_TEMPLATE = "{servername}-{datetime}.psql.bin"
DBBACKUP_MEDIA_PATH = "/code/media/"
DBBACKUP_CLEANUP_KEEP = 7

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

DEBUG = config("DEBUG", default=True, cast=bool)

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_browser_reload",
    ]
    MIDDLEWARE = (
        ["debug_toolbar.middleware.DebugToolbarMiddleware"]
        + MIDDLEWARE
        + ["django_browser_reload.middleware.BrowserReloadMiddleware"]
    )

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}
