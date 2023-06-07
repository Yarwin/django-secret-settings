from django_secret_settings import SecretsEnum


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django_secret_settings",
    "tests",
)

MIDDLEWARE = []

USE_TZ = True

TIME_ZONE = "UTC"

SECRET_KEY = "foobar"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

STATIC_URL = "/static/"

# it might be obvious, but one shouldn't store their secret key as-is in settings
DJANGO_SECRETS_KEY='OPkJTxw15IZiidRqACDjxGADlYFL8Az4TQyfQVzVQVo='


class ExampleSecrets(SecretsEnum):
    SECRET_TYPE_1 = 1
    SECRET_TYPE_2 = 2


DJANGO_SECRET_VALUES = ExampleSecrets
