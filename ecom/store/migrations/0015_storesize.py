# Generated by Django 5.0.6 on 2024-05-21 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
            ],
        ),
    ]
