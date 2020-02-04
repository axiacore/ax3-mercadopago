import requests
from mercadopago import api
from mercadopago.client import BaseClient

from . import exceptions, settings


class CardTokenAPI(api.CardTokenAPI):
    _base_path = '/v1/card_tokens'
    params = {'public_key': settings.PUBLIC_KEY}

    def create(self, **data):
        return self._client.post('/', params=self.params, json=data)

    def get(self, token_id):
        return self._client.get('/{id}', {'id': token_id}, params=self.params)

    def update(self, token_id, public_key, **data):
        return self._client.put('/{id}', {'id': token_id}, params=self.params, json=data)


class AX3Client(BaseClient):
    base_url = 'https://api.mercadopago.com'

    def __init__(self, access_token=None):
        self._session = requests.Session()

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

        url = self.base_url + path.format(**path_args)

        return self._request(method, url, **kwargs)

    @property
    def access_token(self):
        return self._access_token

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
