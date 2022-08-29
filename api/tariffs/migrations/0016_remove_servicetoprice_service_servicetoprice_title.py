# Generated by Django 4.0.6 on 2022-08-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0015_remove_tariff_name_tariff_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicetoprice',
            name='service',
        ),
        migrations.AddField(
            model_name='servicetoprice',
            name='title',
            field=models.CharField(default='', max_length=128, verbose_name='Название'),
        ),
    ]
