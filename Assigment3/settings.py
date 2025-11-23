
# Django requires a settings module to initialize.
# When you call django.setup(), Django reads:
# What DB to use
# Which apps are installed
# What timezone, language, etc.
sssss
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "replace-this-with-any-random-string"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [

    "django.contrib.contenttypes",
    "django.contrib.auth",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
