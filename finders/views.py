from datetime import datetime
from django.shortcuts import render
from django import views
from django.http import FileResponse, HttpResponse
import io

from reportlab.pdfgen import canvas

from orders.models import Order
from expenses.models import Capital


def generate_pdf(request):
    if request.method == "POST":

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

    return HttpResponse("Not the correct method")


class Overview(views.generic.ListView):
    admin = {}

    def get(self, request):
        ctx = self.admin.each_context(request)
        
        ctx["capital"] = Capital.load()
        
        ctx["total_money_received_from_orders"] = (
            f"{Order.objects.get_all_received_money_from_orders()}$"
        )
        ctx["total_missing_money"] = (
            f"{Order.objects.get_missing_money_from_all_providers()}$"
        )
        ctx["email"] = "Email"
        return render(request, "overview.html", ctx)