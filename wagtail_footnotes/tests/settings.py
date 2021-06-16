import os

import django.utils.crypto

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = django.utils.crypto.get_random_string(50)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.users",
    "wagtail.core",
    # "wagtail.contrib.frontend_cache",
    "wagtail_footnotes",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

MEDIA_ROOT = os.path.join(TESTS_PATH, "media")

STATIC_ROOT = os.path.join(TESTS_PATH, "static")

ROOT_URLCONF = "wagtail_footnotes.tests.urls"

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
]
