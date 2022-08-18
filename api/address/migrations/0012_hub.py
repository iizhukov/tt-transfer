# Generated by Django 4.0.6 on 2022-08-15 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0011_city_center_alter_cityzone_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=128, verbose_name='Улица')),
                ('number', models.CharField(default='1', max_length=12, verbose_name='Номер дома')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('city', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город')),
                ('coordinate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate', verbose_name='Координаты')),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
                'db_table': 'address_hub',
            },
        ),
    ]
