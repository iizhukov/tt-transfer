# Generated by Django 4.0.6 on 2022-09-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_hub_slug_alter_city_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hub',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True, verbose_name='Слаг'),
        ),
    ]
