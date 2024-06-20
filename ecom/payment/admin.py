from django.contrib import admin
from django.http import HttpResponse
from .models import ShippingAddress, Order, OrderItem
from django.db.models import Sum
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped", "delivered", "date_delivered"]
    inlines = [OrderItemInline]

    list_display = ["user", "full_name", "email", "shipping_address", "amount_paid", "formatted_date_ordered", "shipped", "formatted_date_shipped", "delivered", "formatted_date_delivered", "order_count", "total_amount_paid"]

    actions = ['generate_invoice_pdf']

    def formatted_date_ordered(self, obj):
        return obj.date_ordered.strftime('%Y-%m-%d %I:%M %p')
    formatted_date_ordered.admin_order_field = 'date_ordered'
    formatted_date_ordered.short_description = 'Date Ordered'

    def formatted_date_shipped(self, obj):
        return obj.date_shipped.strftime('%Y-%m-%d %I:%M %p') if obj.date_shipped else 'N/A'
    formatted_date_shipped.admin_order_field = 'date_shipped'
    formatted_date_shipped.short_description = 'Date Shipped'

    def formatted_date_delivered(self, obj):
        return obj.date_delivered.strftime('%Y-%m-%d %I:%M %p') if obj.date_delivered else 'N/A'
    formatted_date_delivered.admin_order_field = 'date_delivered'
    formatted_date_delivered.short_description = 'Date Delivered'

    def order_count(self, obj):
        return Order.objects.filter(user=obj.user).count()
    order_count.short_description = 'Number of Orders'

    def total_amount_paid(self, obj):
        total = Order.objects.filter(user=obj.user, delivered=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
        return total if total else 0
    total_amount_paid.short_description = 'Total Amount Paid (Delivered Orders Only)'

    def generate_invoice_pdf(self, request, queryset):
        for order in queryset:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

            p = canvas.Canvas(response, pagesize=letter)
            width, height = letter
            margin = 0.5 * inch

            # Header
            p.setFillColorRGB(0, 0.5, 1)  # Blue color
            p.rect(margin, height - margin - 1.5 * inch, width - 2 * margin, 1.5 * inch, fill=True, stroke=False)
            p.setFillColorRGB(1, 1, 1)
            p.setFont("Helvetica-Bold", 24)
            p.drawString(margin + inch, height - margin - inch, "Invoice")
            p.setFont("Helvetica", 12)
            p.drawString(margin + inch, height - margin - 1.25 * inch, "RGB SHOES")
            p.drawString(margin + inch, height - margin - 1.5 * inch, "Brgy.Boyco, Bayawan City, Negros Oreintal")
            p.drawString(margin + inch, height - margin - 1.75 * inch, "City, Country, Postal")

            # Invoice Info
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 12)
            p.drawString(width - margin - 2.5 * inch, height - margin - inch, f"INVOICE NO # {order.id:06d}")
            p.drawString(width - margin - 2.5 * inch, height - margin - 1.25 * inch, f"DATE: {order.date_ordered.strftime('%Y-%m-%d %I:%M %p')}")
            p.drawString(width - margin - 2.5 * inch, height - margin - 1.5 * inch, f"INVOICE DUE DATE: {order.date_ordered.strftime('%Y-%m-%d %I:%M %p')}")

            # Bill To
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin + inch, height - margin - 2.5 * inch, "BILL TO:")
            p.setFont("Helvetica", 12)
            p.drawString(margin + inch, height - margin - 2.75 * inch, f"{order.full_name}")
            p.drawString(margin + inch, height - margin - 3 * inch, f"{order.shipping_address}")

            # Table Header
            table_start = height - margin - 3.75 * inch
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin + inch, table_start, "ITEMS")
            p.drawString(margin + 3 * inch, table_start, "DESCRIPTION")
            p.drawString(margin + 5 * inch, table_start, "QUANTITY")
            p.drawString(margin + 6 * inch, table_start, "PRICE")
            p.drawString(margin + 7 * inch, table_start, "TAX")
            p.drawString(margin + 8 * inch, table_start, "AMOUNT")
            p.line(margin + inch, table_start - 5, margin + 9 * inch, table_start - 5)

            # Table Rows
            y = table_start - 20
            p.setFont("Helvetica", 12)
            for item in order.orderitem_set.all():
                p.drawString(margin + inch, y, item.product.name)
                p.drawString(margin + 3 * inch, y, item.product.description if item.product.description else "")
                p.drawString(margin + 5 * inch, y, str(item.quantity))
                p.drawString(margin + 6 * inch, y, f"${item.price:.2f}")
                p.drawString(margin + 7 * inch, y, "0%")  # Assuming no tax
                p.drawString(margin + 8 * inch, y, f"${item.quantity * item.price:.2f}")
                y -= 20

            # Total
            total_x = margin + 5.5 * inch  # Center the "TOTAL" label
            p.setFont("Helvetica-Bold", 12)
            p.drawString(total_x, y - 20, "TOTAL")
            p.drawString(total_x + inch, y - 20, f"${order.amount_paid:.2f}")

            # Footer
            p.setFont("Helvetica", 10)
            p.drawString(margin + inch, margin, "Powered by RGB SHOES")
            p.drawString(margin + inch, margin - 10, "This invoice was generated with the help of Your System.")

            p.showPage()
            p.save()

            return response

    generate_invoice_pdf.short_description = 'Generate Invoice PDF for selected Orders'

admin.site.register(Order, OrderAdmin)
