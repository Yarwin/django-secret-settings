from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.utils.encoding import force_bytes, force_str
from django.utils.functional import cached_property


class EncryptedField(models.CharField):
    _internal_type = 'BinaryField'

    def get_internal_type(self):
        return self._internal_type

    @cached_property
    def key(self):
        key = getattr(settings, 'DJANGO_SECRETS_KEY', None)
        if not key:
            raise ValueError("No secret key has been provided for Fernet. "
                             "Fernet key must be 32 url-safe base64-encoded bytes.")
        return key

    @cached_property
    def fernet(self):
        return Fernet(self.key)

    def get_db_prep_save(self, value, connection):
        value = super(
            EncryptedField, self
        ).get_db_prep_save(value, connection)
        if value is not None:
            retval = self.fernet.encrypt(force_bytes(value))
            return connection.Database.Binary(retval)

    def decrypt(self, value):
        if value is not None:
            value = bytes(value)
            return self.to_python(force_str(self.fernet.decrypt(value)))


class Secret(models.Model):
    secret_type = models.SmallIntegerField(choices=settings.DJANGO_SECRET_VALUES.display_choices())
    secret = EncryptedField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def decrypt(self) -> str:
        return self._meta.get_field('secret').decrypt(self.secret)

    def __str__(self):
        return f"{self.get_secret_type_display()} created at {self.created_at}"
