from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from providers.models import DeliveryProvider, ShippingProvider, ShippingSource
from utils.models import BaseAdminModel


# Register your models here.
class BaseProvider(BaseAdminModel):
    list_display = ("name", "phone_number")
    search_fields = ("name", "phone_number")


@admin.register(ShippingProvider)
class ShippingProviderAdmin(BaseProvider):
    model = ShippingProvider


def url_to_edit_object(obj):
    url = reverse(
        "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
        args=[obj.id],
    )
    return '<a href="%s">Edit %s</a>' % (url, obj.__unicode__())


@admin.register(DeliveryProvider)
class DeliveryProviderAdmin(BaseProvider):
    model = DeliveryProvider

    list_display = ("name", "phone_number", "get_orders_count")

    def get_orders_count(self, obj):
        count = obj.order_set.count()
        url = f"/orders/order/?delivery_provider_id={obj.id}"
        return format_html('<a href="{}">{} Orders</a>', url, count)

    def get_orders(self, obj):
        return obj.order_set.all()


@admin.register(ShippingSource)
class ShippingSourceAdmin(BaseAdminModel):
    model = ShippingSource

    list_display = ("name",)
    search_fields = ("name",)
