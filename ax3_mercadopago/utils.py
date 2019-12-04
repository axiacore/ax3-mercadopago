from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.utils.module_loading import import_string

from .api import AX3Client
from .cache_keys import CACHE_KEY_BANK_LIST, CACHE_KEY_IDENTIFICATION_TYPE_LIST
from . import data


def refresh_bank_list_cache():
    mercado_pago = AX3Client()
    response = mercado_pago.payment_methods.list()

    for item in response.data:
        if item['id'] != 'pse':
            continue

        bank_list = [(x['id'], x['description']) for x in item.get('financial_institutions', [])]
        if bank_list:
            cache.set(CACHE_KEY_BANK_LIST, bank_list, timeout=None)


def refresh_document_types_cache():
    mercado_pago = AX3Client()
    response = mercado_pago.identification_types.list()

    bank_list = [(x['id'], x['name']) for x in response.data]
    cache.set(CACHE_KEY_IDENTIFICATION_TYPE_LIST, bank_list, timeout=None)


def create_mercadopago_user(user_dict: dict, retries: int = 3) -> str:
    """user_dict must have following keys: first_name, last_name, email"""
    mercadopago = AX3Client()
    response = mercadopago.customers.search(email=user_dict['email'])

    if response.total > 0:
        return response.results[0]['id']

    response = mercadopago.customers.create(**user_dict)
    return response.data['id']


def update_payment(mercadopago_payment_id: int):
    mercado_pago = AX3Client()
    response = mercado_pago.payments.get(mercadopago_payment_id)

    status_map = {
        'rejected': data.REJECTED_CHOICE,
        'pending': data.PENDING_CHOICE,
        'approved': data.PAID_CHOICE,
        'authorized': data.PENDING_CHOICE,
        'in_process': data.PENDING_CHOICE,
        'in_mediation': data.PENDING_CHOICE,
        'cancelled': data.CANCELLED_CHOICE,
        'refunded': data.REFUNDED_CHOICE,
        'charged_back': data.CHARGED_BACK_CHOICE,
    }

    if response.status_code == 200 and 'status' in response.data:
        payment = apps.get_model(settings.PAYMENT_MODEL).objects.filter(
            id=response.data['external_reference'].strip(settings.REFERENCE_PREFIX)
        ).first()

        payment.payment_response = response.data
        payment.status = status_map[response.data['status']]
        payment.save(update_fields=['payment_response', 'status'])

        if payment.status == data.PAID_CHOICE:
            usecase = import_string(settings.PAID_USECASE)(
                payment=payment,
                payment_response=response.data
            )
            usecase.execute()

        elif payment.status in [data.CANCELLED_CHOICE, data.REJECTED_CHOICE]:
            usecase = import_string(settings.REJECTED_USECASE)(
                payment=payment,
                payment_response=response.data
            )
            usecase.execute()
