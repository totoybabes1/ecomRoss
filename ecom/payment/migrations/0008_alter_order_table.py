# Generated by Django 5.0.6 on 2024-05-23 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_order_date_shipped'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='Order',
        ),
    ]
