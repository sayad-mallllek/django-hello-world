from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from orders.models import Order
from providers.models import DeliveryProvider, ShippingProvider, ShippingSource
from utils.models import BaseAdminModel


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

    inlines = [OrderDeliverProviderInline]

    def get_orders_count(self, obj):
        count = obj.order_set.count()
        url = f"/orders/order/?delivery_provider_id={obj.id}"
        return format_html('<a href="{}">{} Orders</a>', url, count)

    def missing_money_from_provider(self, obj):
        return f"{obj.order_set.filter(has_received_price=False).count()}$"

    # def my_view(self, request):
    #     # ...
    #     context = dict(
    #         # Include common variables for rendering the admin template.
    #         self.admin_site.each_context(request),
    #         # Anything else you want in the context...
    #         key=value,
    #     )
    #     return TemplateResponse(request, "admin/index.html", context)


@admin.register(ShippingSource)
class ShippingSourceAdmin(BaseAdminModel):
    model = ShippingSource

    list_display = ("name",)
    search_fields = ("name",)


class Media:
    js = ["js/collapsed-stacked-inlines.js"]
