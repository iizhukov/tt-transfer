# Generated by Django 4.0.6 on 2022-10-08 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0009_tariff_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='citytoprice',
            name='converse',
            field=models.BooleanField(default=False, verbose_name='Обратный?'),
        ),
    ]
