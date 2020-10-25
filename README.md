# AX3 Mercadopago

AX3 Mercadopago A Django app to add support for Mercadopago payments.

## Installation

AX3 Mercadopago is easy to install from the PyPI package:

    $ pip install ax3-mercadopago

After installing the package, the project settings need to be configured.

Add ``ax3_mercadopago`` to your ``INSTALLED_APPS``

```python
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
```

## Configuration

Add mercadopago settings

```python
# app/settings.py

MERCADOPAGO_REFERENCE_PREFIX = ''  # Prefix for Mercadopago external reference 
MERCADOPAGO_PAYMENT_MODEL = ''  # Path to payment model
MERCADOPAGO_PAID_USECASE = ''  # Path to use case for paid payments
MERCADOPAGO_REJECTED_USECASE = ''  # Path to use case for rejected payments

# For Marketplace
# https://www.mercadopago.com.co/developers/es/guides/online-payments/marketplace/checkout-pro/introduction
MERCADOPAGO_MARKETPLACE_SELLER = True
MERCADOPAGO_MARKETPLACE_APP_ID = ''
MERCADOPAGO_MARKETPLACE_REDIRECT_URI = ''  
```

Set ax3_mercadopago in app urls

```python
# app/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),

    # Add this line
    path('mercadopago/', include('ax3_mercadopago.urls', namespace='mercadopago')),
]
```

Use ``PaymentModelMixin`` in your payment model

```python
class Payment(PaymentModelMixin):
```

## Utils

### Get seller token request uri, on shell_plus
```python
from ax3_mercadopago.api import AX3Client

mp = AX3Client()
mp.marketplace_tokens.get_auth_uri()
# response
https://auth.mercadopago.com.co/authorization?client_id=&redirect_uri=https%3A%2F%2Fclientes-staging.takami.co&response_type=code&platform_id=mp
```

### To create Seller Token, on shell_plus use
```python
from app.mercadopago import create_seller_token

brand = Brand.objects.first()
create_seller_token(code='SELLER-CODE', brand=brand)
```


## Releasing a new version

Make sure you increase the version number and create a git tag:

```
$ python3 -m pip install --user --upgrade setuptools wheel twine
$ ./release.sh
```
