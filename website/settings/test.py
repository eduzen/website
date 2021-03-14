from .base import Base


class Test(Base):
    DEBUG = False
    TEMPLATE_DEBUG = False
    DEBUG_LOGGING = False

    STATIC_URL = "static"

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
