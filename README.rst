django-secret-settings
===============

Django Secret Settings is a Django application allowing for convenient creation&retrieval of encrypted secret keys.


Installation
----
Install using pip:

.. code-block:: sh

    pip install django-secret-settings

Then add ``'django_secret_settings'`` to your ``INSTALLED_APPS``, import django-secret's ``'SecretsEnum'`` and define your secrets.

.. code-block:: python

    from django_secrets import SecretsEnum


    INSTALLED_APPS = [
    ...
    "django_secret_settings",
    ]


    class ExampleSecrets(SecretsEnum):
        SECRET_TYPE_1 = 1
        SECRET_TYPE_2 = 2

    DJANGO_SECRET_VALUES = ExampleSecrets


Usage
----

You can access your secrets anywhere in code by:

.. code-block:: python

    >>> from django_secrets import secret_settings
    >>> some_decrypted_key = secret_settings.MY_KEY

