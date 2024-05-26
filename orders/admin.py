from django.contrib import admin

from orders.models import Order, OrderBasket
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
        "id",
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
        ("Status", {"fields": ("status",)}),
        (
            "Customer",
            {"fields": ("customer",)},
        ),
        ("Order Basket", {"fields": ("order_basket",)}),
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
        "created_at",
    )
    search_fields = ("id",)
    list_filter = (
        ("created_at", admin.DateFieldListFilter),
        ("shipped_at", admin.DateFieldListFilter),
        ("received_at", admin.DateFieldListFilter),
        "status",
        "shipping_provider__name",
        "shipping_source__name",
    )

    fieldsets = (
        (
            "Basket Items",
            {
                "fields": (
                    "total_price",
                    "total_paid_price",
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
    )

    @admin.display(ordering="shipping_provider__name", description="Shipping Provider")
    def get_shipping_provider(self, obj):
        return obj.shipping_provider.name

    @admin.display(ordering="shipping_source__name", description="Shipping Source")
    def get_shipping_source(self, obj):
        return obj.shipping_source.name


# from django.contrib import admin
# from django.shortcuts import render


# def overview_admin_view(request):
#     # Access and process data for your overview view here
#     context = {
#         # Add context data based on your needs
#     }
#     return render(request, "pages/overview.html", context)


# admin.site.add_index_view(overview_admin_view)
