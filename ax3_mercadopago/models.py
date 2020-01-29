from django.contrib.postgres.fields import JSONField
from django.db import models

from .data import PAYMENT_STATUS_CHOICES, PENDING_CHOICE, PAID_CHOICE


class PaymentModelMixin(models.Model):
    payment_status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PENDING_CHOICE,
    )

    payment_response = JSONField(default=dict)

    def is_paid(self):
        return self.payment_status == PAID_CHOICE

    class Meta:
        abstract = True
