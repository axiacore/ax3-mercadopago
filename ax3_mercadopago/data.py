PENDING_CHOICE = 10
APPROVED_CHOICE = 20
REJECTED_CHOICE = 30
CANCELLED_CHOICE = 40
REFUNDED_CHOICE = 50
CHARGED_BACK_CHOICE = 60
PAYMENT_STATUS_CHOICES = (
    (PENDING_CHOICE, 'Pendiente'),
    (APPROVED_CHOICE, 'Pagado'),
    (REJECTED_CHOICE, 'Rechazado'),
    (CANCELLED_CHOICE, 'Cancelado'),
    (REFUNDED_CHOICE, 'Reversado'),
    (CHARGED_BACK_CHOICE, 'Reversado'),
)

MERCADOPAGO_STATUS_MAP = {
    'rejected': REJECTED_CHOICE,
    'pending': PENDING_CHOICE,
    'approved': APPROVED_CHOICE,
    'authorized': PENDING_CHOICE,
    'in_process': PENDING_CHOICE,
    'in_mediation': PENDING_CHOICE,
    'cancelled': CANCELLED_CHOICE,
    'refunded': REFUNDED_CHOICE,
    'charged_back': CHARGED_BACK_CHOICE,
}
