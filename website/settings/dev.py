import logfire

from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

logfire.configure(send_to_logfire="if-token-present", environment="local")
logfire.instrument_django()
logfire.instrument_psycopg()

DEBUG = True
ALLOWED_HOSTS = ["*"]

SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
INTERNAL_IPS = ["127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS = True

MEDIA_URL = "https://media.eduzen.ar/"

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
]

MIDDLEWARE = (
    ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    + MIDDLEWARE
    + ["django_browser_reload.middleware.BrowserReloadMiddleware"]
)
