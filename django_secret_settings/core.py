from enum import IntEnum

from django.apps import apps
from django.conf import settings
from django.utils.functional import LazyObject
from django.utils.translation import gettext_lazy as _


class SecretsEnum(IntEnum):
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.lower().replace("_", " ").capitalize()) for choice in cls]

    def get_display_choice(self):
        name_map = {
            choice.value: _(choice.name)
            for choice in self.__class__
        }
        return name_map[self.value]

    @classmethod
    def display_choices(cls):
        return [(choice.value, choice.get_display_choice()) for choice in cls]


def make_secret_property(value, model):
    def secret_property(_self):
        return model.objects.filter(secret_type=value).latest('created_at').decrypt()
    return secret_property


class SecretManager(LazyObject):
    """
    Lazy evaluator of decrypted secret keys stored in the database.
    NOTE: every retrieval performed with SecretManager results in single query.
    This is done on purpose – there isn't any easy and convenient way to notify all the django workers about the change
    outside resetting them and re-instancing SecretManager again.

    Usage:
    >>> from django_secret_settings import secret_settings
    >>> some_decrypted_key = secret_settings.MY_KEY
    """

    def _setup(self, *_args, **_kwargs):
        class SecretWrapper:
            pass

        secrets_model = apps.get_model('django_secret_settings.Secret')
        secrets_wrapper = SecretWrapper

        for (value, name) in settings.DJANGO_SECRET_VALUES.display_choices():
            setattr(secrets_wrapper,
                    str(name),
                    property(
                        make_secret_property(value, secrets_model)
                    ))
        self._wrapped = secrets_wrapper()


secret_settings = SecretManager()
