# Generated by Django 5.0.6 on 2024-05-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_rename_shipping_user_shippingaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
