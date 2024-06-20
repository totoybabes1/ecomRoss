# Generated by Django 5.0.6 on 2024-05-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size',
            new_name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]