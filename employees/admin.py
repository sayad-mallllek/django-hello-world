from django.contrib import admin

from employees.models import Employee
from utils.models import BaseAdminModel


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(BaseAdminModel):
    fieldsets = (
        (
            "Employee Info",
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone_number",
                )
            },
        ),
        ("Salary", {"fields": ("salary",)}),
    )
