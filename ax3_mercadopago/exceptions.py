class MercadopagoError(Exception):
    http_status = None
    json_body = None
    code = None

    def __init__(self, cause_or_message):
        if isinstance(cause_or_message, str):
            super().__init__(cause_or_message)
            return

        cause = cause_or_message

        try:
            self.http_status = cause.response.status_code
            self.json_body = cause.response.json()
            self.text_body = cause.response.text
            self.code = self.json_body['error']
            message = self.json_body['message']
        except (KeyError, ValueError):
            message = str(cause)

        super().__init__(message)


class AuthenticationError(MercadopagoError):
    pass


class NotFoundError(MercadopagoError):
    pass


class BadRequestError(MercadopagoError):
    pass
