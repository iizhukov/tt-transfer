# Generated by Django 4.0.6 on 2022-08-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0012_servicetoprice_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='services',
            field=models.ManyToManyField(null=True, to='tariffs.servicetoprice', verbose_name='Цены к услугам'),
        ),
    ]
