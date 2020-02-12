from django.contrib import admin

from .settings import MARKETPLACE_SELLER
from .models import MercadopagoAccessToken


@admin.register(MercadopagoAccessToken)
class MercadopagoAccessTokenAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_id',
        'access_token',
        'public_key',
        'refresh_token',
        'created_at',
        'expires_in',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'user_id',
                'access_token',
                'public_key',
                'refresh_token',
                'token_type',
                'expires_in',
                'response_json',
            ),
        }),
    )

    list_filter = ['created_at', 'expires_in']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return MARKETPLACE_SELLER
