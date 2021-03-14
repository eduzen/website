# from configurations import values

from .base import Base


class Test(Base):
    DEBUG = False
    TEMPLATE_DEBUG = False
    DEBUG_LOGGING = False
    STATIC_URL = "/static/"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"

    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
