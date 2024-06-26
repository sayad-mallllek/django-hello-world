from io import BytesIO
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.db import models
from xhtml2pdf import pisa
from io import BytesIO
import datetime

from expenses.models import Expense, ExpenseCategory, Capital
from utils.models import BaseAdminModel


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(BaseAdminModel):
    pass


@admin.register(Expense)
class ExpenseAdmin(BaseAdminModel):
    list_filter = ("category",)

    actions = ["print_as_pdf"]

    change_form_template = "admin/expenses/expense/change_form.html"

    def export_expense_as_pdf(self, request, object_id):
        # Fetch the relevant Expense object using object_id
        try:
            expenses = Expense.objects.filter(pk=object_id)
        except Expense.DoesNotExist:
            return HttpResponse("Expense not found", status=404)

        context = {
            "expenses": expenses,
            "total_expenses": expenses.aggregate(r=models.Sum("amount")).get("r"),
        }

        # Render the HTML template with context data
        html = render_to_string("pdf/expense_invoice.html", context)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create a BytesIO buffer for the PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="expense_{timestamp}.pdf"'
        )

        # Convert HTML content to PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

        if not pdf.err:
            response.write(result.getvalue())
            return response
        else:
            return HttpResponse("Error rendering PDF", status=400)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if "export_pdf" in request.GET:
            return self.export_expense_as_pdf(request, object_id)

        # Call the superclass method to continue with the normal flow
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        # if request.POST.get("export_pdf"):
        #     return self.render_pdf(context, download=True)

        if "action" in request.POST and request.POST["action"] == "print_as_pdf":
            # Call your print_as_pdf method here
            # Make sure to pass the queryset containing only the current object
            return self.print_as_pdf(request, Expense.objects.filter(pk=obj.pk))
        return super().response_change(request, obj)

    def print_as_pdf(self, request, queryset):
        context = {
            "expenses": queryset,
            "total_expenses": queryset.aggregate(r=models.Sum("amount")).get("r"),
        }

        # Render the HTML template with context data
        html = render_to_string("pdf/expense_invoice.html", context)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create a BytesIO buffer for the PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="expense_{timestamp}.pdf"'
        )

        # Convert HTML content to PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

        if not pdf.err:
            response.write(result.getvalue())
            return response
        else:
            return HttpResponse("Error rendering PDF", status=400)

    print_as_pdf.short_description = "Print selected items as PDF"


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
