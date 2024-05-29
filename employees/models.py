from django.db import models

from utils.models import BaseModel


# Create your models here.
class Employee(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    salary = models.FloatField(default=0)
