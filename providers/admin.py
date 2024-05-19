from django.contrib import admin

from providers.models import DeliveryProvider, ShippingProvider, ShippingSource
from utils.models import BaseAdminModel


# Register your models here.
class BaseProvider(BaseAdminModel):
    list_display = ("name", "phone_number")
    search_fields = ("name", "phone_number")


@admin.register(ShippingProvider)
class ShippingProviderAdmin(BaseProvider):
    model = ShippingProvider


@admin.register(DeliveryProvider)
class DeliveryProviderAdmin(BaseProvider):
    model = DeliveryProvider


@admin.register(ShippingSource)
class ShippingSourceAdmin(BaseAdminModel):
    model = ShippingSource

    list_display = ("name",)
    search_fields = ("name",)
