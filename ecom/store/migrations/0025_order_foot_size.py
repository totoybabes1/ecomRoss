# Generated by Django 5.0.6 on 2024-06-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_product_foot_size_product_in_stock_product_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='foot_size',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
    ]
