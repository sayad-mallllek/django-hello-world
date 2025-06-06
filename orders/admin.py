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

    actions = ["mark_as_delivered", "print_to_pdf"]

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(request, "Marked as delivered")

    mark_as_delivered.short_description = "Mark as delivered"
    
    def print_to_pdf(self, request, queryset):
        selected_ids = ",".join(str(order.id) for order in queryset)
        url = f"/print-orders-pdf/?ids={selected_ids}"
        return HttpResponse(
            f'<script>window.open("{url}", "_blank").focus();</script>'
        )
    
    print_to_pdf.short_description = "Print selected orders to PDF"

    @admin.display(ordering="customer__full_name", description="Customer")
    def get_customer(self, obj):
        return obj.customer.full_name

    @admin.display(ordering="delivery_provider__name", description="Delivery Provider")
    def get_delivery_provider(self, obj):
        return obj.delivery_provider

    def save_model(self, request, obj, form, change):
        # Get old object to compare total_price if this is an update
        if change:  # If this is an update
            old_obj = Order.objects.get(pk=obj.pk)
            old_total_price = old_obj.total_price
        else:  # If this is a new object
            old_total_price = 0

        # Calculate points difference
        points_difference = int(obj.total_price - old_total_price)

        # Update customer points
        if points_difference != 0:
            customer = obj.customer
            customer.points += points_difference
            customer.save()

        super().save_model(request, obj, form, change)

        # Original basket completion check logic
        order_basket = obj.order_basket
        orders = order_basket.order_set.all()
        if orders.exists() and all(order.has_received_price for order in orders):
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
        "tracking_number",
        "get_shipping_provider",
        "get_shipping_source",
        "shipping_charge",
        "status",
        "total_price",
        "total_paid_price",
        "get_total_profit",
        "shipped_at",
    )
    search_fields = ("id", "tracking_number")
    list_filter = (
        ("shipped_at", admin.DateFieldListFilter),
        ("received_at", admin.DateFieldListFilter),
        "status",
        "shipping_provider__name",
        "shipping_source__name",
    )
    
    actions = ["print_to_pdf"]
    
    def print_to_pdf(self, request, queryset):
        selected_ids = ",".join(str(basket.id) for basket in queryset)
        url = f"/print-order-baskets-pdf/?ids={selected_ids}"
        return HttpResponse(
            f'<script>window.open("{url}", "_blank").focus();</script>'
        )
    
    print_to_pdf.short_description = "Print selected order baskets to PDF"

    readonly_fields = ("get_total_profit",)

    fieldsets = (
        ("Tracking Number", {"fields": ("tracking_number",)}),
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

    def get_fieldsets(self, request, obj=...):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets[1][1]["fields"] = ("total_price",)
            fieldsets[2][1]["fields"] = (
                "number_of_items",
                "items_link",
            )
            fieldsets[4][1]["fields"] = (
                "shipping_source",
                "shipped_at",
                "received_at",
            )
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if not request.user.is_superuser:
            list_display = list_display[:2] + list_display[3:]
        return list_display

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        if not request.user.is_superuser:
            list_filter = list_filter[:3] + list_filter[4:]
        return list_filter

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print("FORM", form)
        return form

    def save_model(self, request, obj, form, change):
        if change:  # Update case
            old_obj = OrderBasket.objects.get(pk=obj.pk)
            old_weight = old_obj.items_weight or 0
        else:  # Creation case
            old_weight = 0

        new_weight = obj.items_weight or 0

        # Calculate points difference (1 point per 100 weight units)
        weight_difference = new_weight - old_weight
        points_difference = int(weight_difference / 100)

        # Update shipping provider points if there's a change
        if points_difference != 0 and obj.shipping_provider:
            provider = obj.shipping_provider
            provider.points += points_difference
            provider.save()

        super().save_model(request, obj, form, change)
