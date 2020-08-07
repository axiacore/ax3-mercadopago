from urllib.parse import urlencode

import requests
from mercadopago import api
from mercadopago.client import BaseClient

from . import exceptions, settings
from .models import MercadopagoAccessToken


class CardTokenAPI(api.CardTokenAPI):
    _base_path = '/v1/card_tokens'
    params = {'public_key': settings.PUBLIC_KEY}

    def create(self, **data):
        return self._client.post('/', params=self.params, json=data)

    def get(self, token_id):
        return self._client.get('/{id}', {'id': token_id}, params=self.params)

    def update(self, token_id, public_key, **data):
        return self._client.put('/{id}', {'id': token_id}, params=self.params, json=data)


class MarketplaceOAuthTokenAPI(api.API):
    _base_path = '/oauth/token'
    _redirect_uri = settings.MARKETPLACE_REDIRECT_URI

    def create(self, code):
        params = {
            'client_secret': settings.ACCESS_TOKEN,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self._redirect_uri,
        }
        return self._client.post('/', params=params)

    def refresh(self, refresh_token):
        params = {
            'client_secret': settings.ACCESS_TOKEN,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return self._client.post('/', params=params)

    def get_auth_uri(self):
        return 'https://auth.mercadopago.com.ar/authorization?{}'.format(
            urlencode({
                'client_id': settings.MARKETPLACE_APP_ID,
                'redirect_uri': self._redirect_uri,
                'response_type': 'code',
                'platform_id': 'mp',
            })
        )


class AX3Client(BaseClient):
    base_url = 'https://api.mercadopago.com'

    def __init__(self, access_token=None):
        self._session = requests.Session()
        if settings.PLATFORM_ID:
            self._session.headers['x-platform-id'] = settings.PLATFORM_ID

        if not access_token:
            access_token = settings.ACCESS_TOKEN
        self._access_token = access_token

    def _handle_request_error(self, error):
        if isinstance(error, requests.HTTPError):
            status = error.response.status_code

            if status == 400:
                raise exceptions.BadRequestError(error)
            if status == 401:
                raise exceptions.AuthenticationError(error)
            if status == 404:
                raise exceptions.NotFoundError(error)

        raise exceptions.MercadopagoError(error)

    def request(self, method, path, path_args=None, **kwargs):
        if path_args is None:
            path_args = {}

        if 'params' not in kwargs:
            kwargs['params'] = {}

        kwargs['params']['access_token'] = self.access_token

        if settings.MARKETPLACE_SELLER and api.PaymentAPI._base_path in path:
            seller_token = MercadopagoAccessToken.objects.first()
            if not seller_token:
                raise exceptions.AuthenticationError(
                    'Ensure create the first token using create_seller_token function, maybe you '
                    'need generate code to create token, use marketplace_tokens.get_auth_uri '
                    'to get auth url and paste it on the browser'
                )

            kwargs['params']['access_token'] = seller_token.access_token

        url = self.base_url + path.format(**path_args)

        return self._request(method, url, **kwargs)

    @property
    def access_token(self):
        return self._access_token

    @property
    def marketplace_tokens(self):
        return MarketplaceOAuthTokenAPI(self)

    @property
    def card_tokens(self):
        return CardTokenAPI(self)

    @property
    def customers(self):
        return api.CustomerAPI(self)

    @property
    def identification_types(self):
        return api.IdentificationTypeAPI(self)

    @property
    def invoices(self):
        return api.InvoiceAPI(self)

    @property
    def merchant_orders(self):
        return api.MerchantOrderAPI(self)

    @property
    def payment_methods(self):
        return api.PaymentMethodAPI(self)

    @property
    def payments(self):
        return api.PaymentAPI(self)

    @property
    def advanced_payments(self):
        return api.AdvancedPaymentAPI(self)

    @property
    def chargebacks(self):
        return api.ChargebackAPI(self)

    @property
    def plans(self):
        return api.PlanAPI(self)

    @property
    def preapprovals(self):
        return api.PreapprovalAPI(self)

    @property
    def preferences(self):
        return api.PreferenceAPI(self)

    @property
    def money_requests(self):
        return api.MoneyRequestAPI(self)

    @property
    def shipping_options(self):
        return api.ShippingOptionAPI(self)

    @property
    def pos(self):
        return api.PosAPI(self)

    @property
    def account(self):
        return api.AccountAPI(self)

    @property
    def users(self):
        return api.UsersAPI(self)

    @property
    def sites(self):
        return api.SiteAPI(self)
