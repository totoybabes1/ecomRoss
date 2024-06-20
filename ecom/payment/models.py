from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)


#create order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    Shipping_address = models.TextField(max_length=25000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateField(blank=True, null=True)
    delivered = models.BooleanField(default=False)
    delivered_date = models.DateField(blank=True, null=True)
    DisplayTable = ['user', 'full_name', 'email', 'Shipping_address', 'amount_paid', 'date_ordered', 'shipped', 'date_shipped', 'delivered']
    SearchableFields = ['full_name']

    class Meta:
        db_table = 'Order'

    def total_income(self):
        return sum(item.price for item in self.orderitem_set.all())
    
    def __str__(self):
        status = "Delivered" if self.delivered else "Pending"
        return f'Order - {str(self.id)} ({status})'



@receiver(pre_save, sender=Order)
def set_shipped_and_delivered_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now.date()
        if instance.delivered and not obj.delivered:
            instance.delivered_date = now.date()




    #create order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'