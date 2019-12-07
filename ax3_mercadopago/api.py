from requests import HTTPError
from mercadopago.api import Client

from . import settings, exceptions


class AX3Client(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            *args,
            **kwargs
        )

    def _handle_request_error(self, error):
        if isinstance(error, HTTPError):
            status = error.response.status_code

            if status == 400:
                raise exceptions.BadRequestError(error)
            if status == 401:
                raise exceptions.AuthenticationError(error)
            if status == 404:
                raise exceptions.NotFoundError(error)

        raise exceptions.MercadopagoError(error)

    @property
    def access_token(self) -> str:
        if settings.ACCESS_TOKEN:
            return settings.ACCESS_TOKEN

        if not self.is_authenticated():
            self.authenticate()

        return self._auth['access_token']
