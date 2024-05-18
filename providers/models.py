from django.db import models

from utils.models import BaseModel


# Create your models here.
class BaseProvider(BaseModel):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ShippingProvider(BaseProvider):
    price_per_kg = models.FloatField()
    address = models.CharField(max_length=255)


class DeliveryProvider(BaseProvider):
    pass
