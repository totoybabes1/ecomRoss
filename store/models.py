from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)  # Fixed typo
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    is_customer = models.BooleanField(default=True)  # New field to indicate if the user is a customer
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Default user ID
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=550, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    foot_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    inventory = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.in_stock = self.inventory > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    foot_size = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.product.in_stock or self.quantity > self.product.inventory:
            raise ValueError("Cannot place an order for out-of-stock products or quantities exceeding inventory.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order of {self.quantity} {self.product.name}(s) by {self.customer.first_name}'
