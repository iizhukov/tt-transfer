# Generated by Django 4.0.6 on 2022-07-28 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_alter_address_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='Россия', max_length=128, verbose_name='Страна')),
                ('region', models.CharField(max_length=128, null=True, verbose_name='Регион')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'db_table': 'address_city',
            },
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Координата',
                'verbose_name_plural': 'Координаты',
                'db_table': 'car_zone_coordinate',
            },
        ),
        migrations.CreateModel(
            name='PriceToCarClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_class', models.CharField(choices=[('business', 'Бизнес'), ('standart', 'Стандарт')], max_length=32, verbose_name='Класс автомобиля')),
                ('price', models.IntegerField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Цена к классу',
                'verbose_name_plural': 'Цены к классам',
                'db_table': 'car_zone_price2car_class',
            },
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='region',
        ),
        migrations.CreateModel(
            name='CityZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('red', 'Красная'), ('green', 'Оранжевая'), ('yellow', 'Желтая'), ('blue', 'Синяя')], max_length=12, verbose_name='Цвет')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город')),
                ('coordinates', models.ManyToManyField(to='address.coordinate')),
                ('prices', models.ManyToManyField(to='address.pricetocarclass')),
            ],
            options={
                'verbose_name': 'Зона города',
                'verbose_name_plural': 'Зоны городов',
                'db_table': 'car_zone',
            },
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город'),
        ),
    ]
