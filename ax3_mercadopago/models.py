from django.contrib.postgres.fields import JSONField
from django.db import models

from .data import PAYMENT_STATUS_CHOICES, PENDING_CHOICE, APPROVED_CHOICE
from .managers import MercadopagoAccessTokenManager


class PaymentModelMixin(models.Model):
    payment_status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING_CHOICE,
    )

    payment_response = JSONField(default=dict)

    def is_paid(self):
        return self.payment_status == APPROVED_CHOICE

    class Meta:
        abstract = True


class MercadopagoAccessToken(models.Model):
    user_id = models.PositiveIntegerField()

    access_token = models.CharField(max_length=120)

    public_key = models.CharField(max_length=60)

    refresh_token = models.CharField(max_length=60)

    token_type = models.CharField(max_length=32)

    expires_in = models.DateTimeField()

    response_json = JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = MercadopagoAccessTokenManager.as_manager()

    def __str__(self):
        return f'{self.user_id} ({self.expires_in})'

    class Meta:
        ordering = ['-expires_in']
        verbose_name = 'access token'
        verbose_name_plural = 'access tokens'
