from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'inventory', 'in_stock', 'is_sale', 'sale_price')
    list_filter = ('category', 'in_stock', 'is_sale')
    search_fields = ('name', 'category__name')
    actions = ['mark_as_sale', 'mark_as_not_sale']

    def mark_as_sale(self, request, queryset):
        queryset.update(is_sale=True)
    mark_as_sale.short_description = "Mark selected products as sale"

    def mark_as_not_sale(self, request, queryset):
        queryset.update(is_sale=False)
    mark_as_not_sale.short_description = "Mark selected products as not sale"

    def save_model(self, request, obj, form, change):
        obj.in_stock = obj.inventory > 0
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', 'is_customer']

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['customer_count'] = Profile.objects.filter(is_customer=True).count()
        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
