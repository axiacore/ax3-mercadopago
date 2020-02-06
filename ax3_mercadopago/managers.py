from django.db.models.query import QuerySet
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class MercadopagoAccessTokenManager(QuerySet):
    def find_all_to_refresh(self) -> QuerySet:
        return self.filter(expires_in__month=(timezone.localtime() + relativedelta(months=1)).month)
