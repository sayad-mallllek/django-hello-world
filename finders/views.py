from django.shortcuts import render
from django import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
import io


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
        ctx["full_name"] = "Full Name"
        ctx["email"] = "Email"
        return render(request, "overview.html", ctx)
