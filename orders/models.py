from django.db import models

from utils.models import BaseModel


# Create your models here.
class Order(BaseModel):
    id = models.AutoField(primary_key=True)
    total_price = models.FloatField()
    number_of_items = models.IntegerField()
    items_link = models.CharField(max_length=255)
    delivery_charge = models.FloatField()
    ordered_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    has_received_price = models.BooleanField(default=False)
    bill_id = models.CharField(max_length=255)
    customer_delivery_charge = models.FloatField()

    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)
    order_basket = models.ForeignKey("OrderBasket", on_delete=models.CASCADE)
    delivery_provider = models.ForeignKey(
        "providers.DeliveryProvider", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.order_id


class OrderBasket(BaseModel):
    id = models.AutoField(primary_key=True)
    total_price = models.FloatField()
    number_of_items = models.IntegerField()
    items_link = models.CharField(max_length=255)
    items_weight = models.FloatField()
    shipping_charge = models.FloatField()
    shipped_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)

    shipping_provider = models.ForeignKey(
        "providers.ShippingProvider", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.id
