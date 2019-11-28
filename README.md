# AX3 Mercadopago

AX3 Mercadopago A Django app to add support for Mercadopago payments.

## Installation

AX3 Mercadopago is easy to install from the PyPI package:

    $ pip install ax3-mercadopago

After installing the package, the project settings need to be configured.

Add ``ax3_mercadopago`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # ax3_mercadopago app can be in any position in the INSTALLED_APPS list.
        'ax3_mercadopago',
    ]

## Configuration

Add Mercadopago client and secret:

    MERCADOPAGO_CLIENT_ID
    MERCADOPAGO_CLIENT_SECRET
