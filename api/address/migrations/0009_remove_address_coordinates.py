# Generated by Django 4.0.6 on 2022-08-10 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0008_address_coordinate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='coordinates',
        ),
    ]
