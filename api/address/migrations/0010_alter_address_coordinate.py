# Generated by Django 4.0.6 on 2022-08-10 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0009_remove_address_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='coordinate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate', verbose_name='Координаты'),
        ),
    ]
