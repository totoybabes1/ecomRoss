# Generated by Django 5.0.6 on 2024-06-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_order_foot_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
