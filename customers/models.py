from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from utils.models import BaseModel


# Create your models here.
class Customer(BaseModel):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    notes = ArrayField(models.CharField(max_length=255))

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
