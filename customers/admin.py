from django.contrib import admin
from django.db import models
from customers.models import Customer
from utils.models import BaseAdminModel


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(BaseAdminModel):
    model = Customer
    list_display = ("full_name",)
    search_fields = ("full_name",)
    list_filter = ("full_name",)

    fieldsets = (
        (
            "Customer Info",
            {"fields": ("full_name", "phone_number", "address", "email")},
        ),
        ("Notes", {"fields": ("notes",)}),
    )
