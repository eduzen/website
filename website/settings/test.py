from configurations import values

from .base import Base


class Test(Base):
    DEBUG = False
    TEMPLATE_DEBUG = False
    DEBUG_LOGGING = False
    STATIC_URL = "/static/"

    DATABASES = values.DatabaseURLValue(conn_max_age=600, ssl_require=False)

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

    STORAGE = {
        "default": {
            "BACKEND": "inmemorystorage.InMemoryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
