# Generated by Django 5.0.6 on 2024-06-06 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_remove_profile_countyr_profile_country_shoesize'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShoeSize',
        ),
    ]
