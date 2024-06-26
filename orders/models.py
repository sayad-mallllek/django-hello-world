from django.db import models

from utils.models import BaseModel


class OrderStatus(models.TextChoices):
    PENDING = "pending"
    BOXING = "boxing"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    REJECTED = "rejected"


class OrderBasketStatus(models.TextChoices):
    SHIPPING = "shipping"
    RECEIVED = "received"
    COMPLETED = "completed"
    REJECTED = "rejected"


class OrderManager(models.Manager):
    def get_total_price(self):
        return self.get_queryset().aggregate(r=models.Sum("total_price")).get("r")

    def get_total_paid_price(self):
        return self.get_queryset().aggregate(r=models.Sum("total_paid_price")).get("r")

    def get_missing_money_from_all_providers(self):
        return (
            self.get_queryset()
            .filter(has_received_price=False)
            .aggregate(r=models.Sum("total_price"))
            .get("r")
        )
        
    def get_all_received_money_from_orders(self):
         return (
            self.get_queryset()
            .filter(has_received_price=True)
            .aggregate(r=models.Sum("customer_delivery_charge"))
            .get("r")
        )


# Create your models here.
class Order(BaseModel):

    objects = OrderManager()

    id = models.AutoField(primary_key=True)
    total_price = models.FloatField()
    number_of_items = models.IntegerField()
    items_link = models.CharField(max_length=255, null=True, blank=True)
    delivery_charge = models.FloatField(null=True, blank=True)
    ordered_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    has_received_price = models.BooleanField(default=False)
    bill_id = models.CharField(max_length=255, null=True, blank=True)
    customer_delivery_charge = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    notes = models.TextField(null=True, blank=True, max_length=10000)

    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)
    order_basket = models.ForeignKey("OrderBasket", on_delete=models.CASCADE)
    delivery_provider = models.ForeignKey(
        "providers.DeliveryProvider", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id}"


class OrderBasket(BaseModel):
    id = models.AutoField(primary_key=True)
    total_price = models.FloatField()
    total_paid_price = models.FloatField(null=True, blank=True)
    number_of_items = models.IntegerField()
    items_link = models.CharField(max_length=255, null=True, blank=True)
    items_weight = models.FloatField(null=True, blank=True)
    shipping_charge = models.FloatField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrderBasketStatus.choices,
        default=OrderBasketStatus.SHIPPING,
    )
    notes = models.TextField(null=True, blank=True, max_length=10000)

    shipping_source = models.ForeignKey(
        "providers.ShippingSource", on_delete=models.CASCADE, null=True, blank=True
    )
    shipping_provider = models.ForeignKey(
        "providers.ShippingProvider", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id} - {self.shipped_at}"
