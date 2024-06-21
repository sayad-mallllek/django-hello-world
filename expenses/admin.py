from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from expenses.models import Expense, ExpenseCategory, Capital
from utils.models import BaseAdminModel


# Register your models here.


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(BaseAdminModel):
    pass


@admin.register(Expense)
class ExpenseAdmin(BaseAdminModel):
    list_filter = ("category",)


@admin.register(Capital)
class CapitalAdmin(BaseAdminModel):

    def has_add_permission(self, request):
        # Disallow adding new objects
        return False

    def has_delete_permission(self, request, obj=None):
        # Disallow deleting objects
        return False

    def response_action(self, request, queryset):
        # Redirect to the change view of the single Capital instance
        return redirect(reverse("admin:expenses_capital_change", args=(1,)))
