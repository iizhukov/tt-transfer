# Generated by Django 4.0.6 on 2022-10-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0016_intracitytariff_city_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='intracitytariff',
            name='city_price',
            field=models.ManyToManyField(to='tariffs.pricetocarclass', verbose_name='Цены к классу авто'),
        ),
    ]
