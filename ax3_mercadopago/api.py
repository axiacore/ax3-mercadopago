from mercadopago.api import Client
from mercadopago.errors import BadRequestError, AuthenticationError, NotFoundError

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
        if isinstance(error, AuthenticationError):
            raise exceptions.AuthenticationError(error)

        if isinstance(error, BadRequestError):
            raise exceptions.BadRequestError(error)

        if isinstance(error, NotFoundError):
            raise exceptions.NotFoundError(error)

        raise exceptions.MercadopagoError(error)

    @property
    def access_token(self) -> str:
        if settings.ACCESS_TOKEN:
            return settings.ACCESS_TOKEN

        if not self.is_authenticated():
            self.authenticate()

        return self._auth['access_token']
