# Generated by Django 5.0.6 on 2024-05-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_remove_product_sizes_delete_store_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_customer',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
