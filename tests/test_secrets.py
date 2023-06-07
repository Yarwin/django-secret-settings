from django.test import TransactionTestCase
from django.conf import settings

from django_secret_settings import secret_settings
from django_secret_settings.models import Secret


class TestEncryptedKey(TransactionTestCase):

    def test_saving_and_retrieving_secret_key(self):
        secret = "my secret"
        other_secret = "my other secret"
        Secret.objects.create(
            secret_type=settings.DJANGO_SECRET_VALUES.SECRET_TYPE_2.value,
            secret=secret
        )
        self.assertNotEqual(secret,
                            Secret.objects.filter(secret_type=settings.DJANGO_SECRET_VALUES.SECRET_TYPE_2).latest('created_at').secret)
        self.assertEqual(secret_settings.SECRET_TYPE_2, secret)
        Secret.objects.create(
            secret_type=settings.DJANGO_SECRET_VALUES.SECRET_TYPE_2.value,
            secret=other_secret
        )
        self.assertNotEqual(secret_settings.SECRET_TYPE_2, secret)
        self.assertNotEqual(other_secret,
                            Secret.objects.filter(secret_type=settings.DJANGO_SECRET_VALUES.SECRET_TYPE_2).latest('created_at').secret)
        self.assertEqual(secret_settings.SECRET_TYPE_2, other_secret)

