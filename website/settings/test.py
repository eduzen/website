from .base import *
from .base import STORAGES  # noqa


DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_LOGGING = False

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# STORAGES["default"]["backend"] = "inmemorystorage.InMemoryStorage"

# MIDDLEWARE = [
#     "django_htmx.middleware.HtmxMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
# ]
