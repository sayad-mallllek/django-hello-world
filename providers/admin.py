from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from orders.models import Order
from providers.models import DeliveryProvider, ShippingProvider, ShippingSource
from utils.models import BaseAdminModel
from django.db.models import Sum


# Register your models here.
class BaseProvider(BaseAdminModel):
    list_display = ("name", "phone_number")
    search_fields = ("name", "phone_number")


@admin.register(ShippingProvider)
class ShippingProviderAdmin(BaseProvider):
    model = ShippingProvider


class OrderDeliverProviderInline(admin.StackedInline):
    model = Order
    extra = 0

    classes = [
        "collapse",
    ]

    fieldsets = (
        (
            "Order Info",
            {
                "fields": (
                    "bill_id",
                    "status",
                    # "get_order_url",
                ),
            },
        ),
        (
            "Delivery Charges",
            {
                "fields": (
                    "delivered_at",
                    "has_received_price",
                    "delivery_charge",
                    "customer_delivery_charge",
                ),
            },
        ),
    )


class ReceivedOrderDeliverProviderInline(OrderDeliverProviderInline):
    verbose_name = "Received Price Order"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(has_received_price=True)


class PendingOrderDeliverProviderInline(OrderDeliverProviderInline):
    verbose_name = "Pending Price Order"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(has_received_price=False)


@admin.register(DeliveryProvider)
class DeliveryProviderAdmin(BaseProvider):
    model = DeliveryProvider

    list_display = ("name", "phone_number", "get_orders_count")
    readonly_fields = ("missing_money_from_provider",)

    fieldsets = (
        (
            "Info",
            {"fields": ("name", "phone_number", "missing_money_from_provider")},
        ),
    )

    change_form_template = "providers/index.html"

    inlines = [ReceivedOrderDeliverProviderInline, PendingOrderDeliverProviderInline]

    def get_orders_count(self, obj):
        count = obj.order_set.count()
        url = f"/orders/order/?delivery_provider_id={obj.id}"
        return format_html('<a href="{}">{} Orders</a>', url, count)

    def missing_money_from_provider(self, obj):
        return f"{obj.order_set.filter(has_received_price=False).aggregate(r=Sum('total_price'))}$"


@admin.register(ShippingSource)
class ShippingSourceAdmin(BaseAdminModel):
    model = ShippingSource

    list_display = ("name",)
    search_fields = ("name",)


class Media:
    js = ["js/collapsed-stacked-inlines.js"]
