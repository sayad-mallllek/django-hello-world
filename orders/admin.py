from django.contrib import admin

from orders.models import Order, OrderBasket
from utils.models import BaseAdminModel, BaseAdminTabularInline


# Register your models here.
@admin.register(Order)
class OrderAdmin(BaseAdminModel):
    model = Order
    list_display = (
        "id",
        "bill_id",
        "get_customer",
        "get_delivery_provider",
        "total_price",
    )
    search_fields = ("id",)
    list_filter = (
        "id",
        "customer_id__full_name",
        "delivery_provider_id__name",
    )

    actions = ["mark_as_delivered"]

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(request, "Marked as delivered")

    mark_as_delivered.short_description = "Mark as delivered"

    @admin.display(ordering="customer__full_name", description="Customer")
    def get_customer(self, obj):
        return obj.customer.full_name

    @admin.display(ordering="delivery_provider__name", description="Delivery Provider")
    def get_delivery_provider(self, obj):
        return obj.delivery_provider.name

    fieldsets = (
        (
            "Items",
            {
                "fields": (
                    "total_price",
                    "number_of_items",
                    "items_link",
                    "bill_id",
                )
            },
        ),
        (
            "Delivery",
            {
                "fields": (
                    "delivered_at",
                    "delivery_charge",
                    "delivery_provider",
                    "customer_delivery_charge",
                    "has_received_price",
                )
            },
        ),
        (
            "Customer",
            {"fields": ("customer",)},
        ),
        ("Order Basket", {"fields": ("order_basket",)}),
    )


class InlineOrderAdmin(BaseAdminTabularInline):
    model = Order
    extra = 0


@admin.register(OrderBasket)
class OrderBasketAdmin(BaseAdminModel):
    inlines = [
        InlineOrderAdmin,
    ]
    model = OrderBasket
    list_display = (
        "id",
        "get_shipping_provider",
        "total_price",
    )
    search_fields = ("id",)
    list_filter = (
        "id",
        "shipping_provider_id__name",
    )

    @admin.display(ordering="shipping_provider__name", description="Shipping Provider")
    def get_shipping_provider(self, obj):
        return obj.shipping_provider.name
