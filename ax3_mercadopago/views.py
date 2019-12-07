import json

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse

from .utils import update_payment
from .exceptions import NotFoundError, BadRequestError


class MercadopagoNotificationView(View):
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            payment_data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError, KeyError) as exc:
            return HttpResponseBadRequest(exc)

        notification_type = payment_data.get('type')
        notification_action = payment_data.get('action')
        if (
            notification_type and notification_type == 'payment' and
            notification_action and notification_action == 'payment.updated'
        ):
            try:
                update_payment(payment_data['data']['id'])
                return HttpResponse('Thank you :)')
            except (NotFoundError, BadRequestError) as exc:
                return HttpResponseBadRequest(exc)

        return HttpResponseBadRequest()
