from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib import admin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'countyr', 'is_customer']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_customer', 'phone', 'city')



# Optionally, you could also add a method to display the count of customers
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

    def changelist_view(self, request, extra_context=None):
        # Add the count of customers to the context
        extra_context = extra_context or {}
        extra_context['customer_count'] = Profile.objects.filter(is_customer=True).count()
        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)



class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
