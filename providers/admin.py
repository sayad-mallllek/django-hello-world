from django.contrib import admin

from providers.models import DeliveryProvider, ShippingProvider
from utils.models import BaseAdminModel


# Register your models here.
class BaseProvider(BaseAdminModel):
    list_display = ("name", "phone_number")
    search_fields = ("name", "phone_number")
    list_filter = ("name",)


@admin.register(ShippingProvider)
class ShippingProviderAdmin(BaseProvider):
    model = ShippingProvider


@admin.register(DeliveryProvider)
class DeliveryProviderAdmin(BaseProvider):
    model = DeliveryProvider
