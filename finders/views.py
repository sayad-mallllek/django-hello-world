from datetime import datetime, timedelta
from django.shortcuts import render
from django import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import FileResponse, HttpResponse
from django.core.paginator import Paginator
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from reportlab.pdfgen import canvas
from orders.models import Order
from expenses.models import Capital
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
        
        ctx["capital"] = Capital.load()
        
        ctx["total_money_received_from_orders"] = (
            f"{Order.objects.get_all_received_money_from_orders()}$"
        )
        ctx["total_missing_money"] = (
            f"{Order.objects.get_missing_money_from_all_providers()}$"
        )
        ctx["email"] = "Email"
        return render(request, "overview.html", ctx)
class RangeSummary(views.generic.ListView):
    admin = {}
    
    def get(self, request):
        ctx = self.admin.each_context(request)
        
        # Get date parameters from request
        date_from_str = request.GET.get('date_from', '')
        date_to_str = request.GET.get('date_to', '')
        page_number = request.GET.get('page', 1)
        
        # Set default dates if not provided
        if not date_from_str:
            date_from = datetime.today() - timedelta(days=30)  # Default to last 30 days
        else:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            
        if not date_to_str:
            date_to = datetime.today()
        else:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
            # Make the end date inclusive by setting it to end of day
            date_to = date_to.replace(hour=23, minute=59, second=59)
        
        # Filter orders by date range
        orders_query = Order.objects.filter(
            created_at__gte=date_from,
            created_at__lte=date_to
        ).order_by('-created_at')
        
        # Paginate the results
        paginator = Paginator(orders_query, 25)  # Show 25 orders per page
        orders_page = paginator.get_page(page_number)
        
        # Add context variables
        ctx.update({
            'orders': orders_page,
            'date_from': date_from,
            'date_to': date_to,
            'is_filtered': bool(date_from_str or date_to_str)
        })
        
        return render(request, "range-summary.html", ctx)
    

def export_range_summary(request):
    # Get date parameters from request
    date_from_str = request.GET.get('date_from', '')
    date_to_str = request.GET.get('date_to', '')
    
    # Set default dates if not provided
    if not date_from_str:
        date_from = datetime.today() - timedelta(days=30)
    else:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
        
    if not date_to_str:
        date_to = datetime.today()
    else:
        date_to = datetime.strptime(date_to_str, '%Y-%m-d')
        date_to = date_to.replace(hour=23, minute=59, second=59)
    
    # Filter orders by date range - no pagination for export
    orders = Order.objects.filter(
        created_at__gte=date_from,
        created_at__lte=date_to
    ).order_by('-created_at')
    
    # Create a workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders Report"
    
    # Add header with date range
    ws.merge_cells('A1:F1')
    header_cell = ws['A1']
    header_cell.value = f"Orders Report ({date_from.strftime('%Y-%m-%d')} to {date_to.strftime('%Y-%m-%d')})"
    header_cell.font = Font(size=14, bold=True)
    header_cell.alignment = Alignment(horizontal='center')
    
    # Create column headers
    headers = ['ID', 'Customer', 'Status', 'Total Price ($)', 'Created At', 'Notes']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws[f'{col_letter}3'] = header
        ws[f'{col_letter}3'].font = Font(bold=True)
        ws[f'{col_letter}3'].fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
    
    # Add data rows
    row_num = 4
    for order in orders:
        ws[f'A{row_num}'] = order.id
        ws[f'B{row_num}'] = order.customer.full_name if order.customer else 'N/A'
        ws[f'C{row_num}'] = order.get_status_display()
        ws[f'D{row_num}'] = order.total_price
        ws[f'E{row_num}'] = order.created_at.strftime('%Y-%m-%d %H:%M')
        ws[f'F{row_num}'] = order.notes if hasattr(order, 'notes') else ''
        row_num += 1
    
    # Add summary row
    ws[f'A{row_num+1}'] = f"Total Orders: {orders.count()}"
    ws[f'A{row_num+1}'].font = Font(bold=True)
    
    ws[f'C{row_num+1}'] = "Total Value:"
    ws[f'C{row_num+1}'].font = Font(bold=True)
    
    ws[f'D{row_num+1}'] = sum(order.total_price for order in orders)
    ws[f'D{row_num+1}'].font = Font(bold=True)
    
    # Auto-size columns
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 15
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"orders_report_{date_from.strftime('%Y%m%d')}_to_{date_to.strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Save the workbook to the response
    wb.save(response)
    return response