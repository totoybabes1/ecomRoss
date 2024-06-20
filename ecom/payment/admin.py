from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.db.models import Sum

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.register(Order)
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["date_ordered", "get_total_income"]
    fields = ["user", "full_name", "email", "Shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped", "delivered", "delivered_date", "get_total_income"]
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'full_name', 'email', 'date_ordered', 'amount_paid', 'shipped', 'delivered', 'get_total_income']
    search_fields = ['user__username', 'full_name', 'email']
    list_filter = ['shipped', 'delivered']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_income=Sum('orderitem__price')
        )
        return queryset

    def get_total_income(self, obj):
        return obj.total_income if hasattr(obj, 'total_income') else None

    get_total_income.short_description = 'Total Income'

admin.site.register(Order, OrderAdmin)
