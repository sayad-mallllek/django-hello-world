from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.http.response import HttpResponse

from orders.models import Order, OrderBasket, OrderBasketStatus
from utils.models import BaseAdminModel, BaseAdminInline


# Register your models here.
@admin.register(Order)
class OrderAdmin(BaseAdminModel):
    model = Order
    list_display = (
        "id",
        "bill_id",
        "get_customer",
        "get_delivery_provider",
        "status",
        "total_price",
    )
    search_fields = ("id",)
    list_filter = (
        "customer_id__full_name",
        "status",
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
        return obj.delivery_provider

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Check if all orders in the basket have received prices
        order_basket = (
            obj.order_basket
        )  # Assuming `order_basket` is the FK to OrderBasket in Order model
        orders = (
            order_basket.order_set.all()
        )  # Assuming a related_name of `order_set` from OrderBasket to Order
        if orders.exists() and all(order.has_received_price for order in orders):
            # If all orders have received prices, set the basket status to COMPLETED
            order_basket.status = OrderBasketStatus.COMPLETED
            order_basket.save()

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
        ("Status", {"fields": ("status",)}),
        (
            "Customer",
            {"fields": ("customer",)},
        ),
        ("Order Basket", {"fields": ("order_basket",)}),
        ("Notes", {"fields": ("notes",)}),
    )


class InlineOrderAdmin(BaseAdminInline):
    model = Order
    extra = 0

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
        ("Status", {"fields": ("status",)}),
        (
            "Customer",
            {"fields": ("customer",)},
        ),
        ("Order Basket", {"fields": ("order_basket",)}),
    )


@admin.register(OrderBasket)
class OrderBasketAdmin(BaseAdminModel):
    inlines = [
        InlineOrderAdmin,
    ]
    model = OrderBasket
    list_display = (
        "id",
        "get_shipping_provider",
        "get_shipping_source",
        "status",
        "total_price",
        "shipped_at",
    )
    search_fields = ("id",)
    list_filter = (
        ("shipped_at", admin.DateFieldListFilter),
        ("received_at", admin.DateFieldListFilter),
        "status",
        "shipping_provider__name",
        "shipping_source__name",
    )

    readonly_fields = ("get_total_profit",)

    fieldsets = (
        (
            "Basket Charge",
            {"fields": ("total_price", "total_paid_price", "get_total_profit")},
        ),
        (
            "Basket Items",
            {
                "fields": (
                    "number_of_items",
                    "items_link",
                    "items_weight",
                )
            },
        ),
        ("Status", {"fields": ("status",)}),
        (
            "Shipping",
            {
                "fields": (
                    "shipping_provider",
                    "shipping_source",
                    "shipping_charge",
                    "shipped_at",
                    "received_at",
                )
            },
        ),
        ("Notes", {"fields": ("notes",)}),
    )

    @admin.display(ordering="shipping_provider__name", description="Shipping Provider")
    def get_shipping_provider(self, obj):
        return obj.shipping_provider.name

    @admin.display(ordering="shipping_source__name", description="Shipping Source")
    def get_shipping_source(self, obj):
        return obj.shipping_source.name

    @admin.display(description="Total Profit")
    def get_total_profit(self, obj):
        if obj.total_price is None:
            return 0
        if obj.total_paid_price is None:
            return obj.total_price
        return obj.total_price - obj.total_paid_price
