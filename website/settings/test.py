from .base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_LOGGING = False

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

STORAGES = {
    "default": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.db.sqlite3",
        "OPTIONS": {
            "init_command": (
                "PRAGMA synchronous=3;"
                "PRAGMA cache_size=2000;"
                "PRAGMA journal_mode=WAL;"
            ),
        },
    }
}
