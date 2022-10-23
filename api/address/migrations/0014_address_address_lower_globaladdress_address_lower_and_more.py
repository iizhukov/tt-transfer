# Generated by Django 4.0.6 on 2022-10-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0013_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_lower',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Сырые данные lower'),
        ),
        migrations.AddField(
            model_name='globaladdress',
            name='address_lower',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Адрес lower'),
        ),
        migrations.AddField(
            model_name='hub',
            name='title_lower',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Название lower'),
        ),
    ]
