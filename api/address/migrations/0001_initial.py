# Generated by Django 4.0.6 on 2022-09-05 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=128, null=True, verbose_name='Улица')),
                ('number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Номер дома')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
                'db_table': 'address',
            },
        ),
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
            name='CityZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('red', 'Красная'), ('green', 'Зеленая'), ('yellow', 'Желтая'), ('blue', 'Синяя')], max_length=12, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Зона города',
                'verbose_name_plural': 'Зоны городов',
                'db_table': 'city_zone',
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
                'db_table': 'city_zone_coordinate',
            },
        ),
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('city', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город')),
                ('coordinate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate', verbose_name='Координаты')),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
                'db_table': 'address_hub',
            },
        ),
        migrations.CreateModel(
            name='HubZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('red', 'Красная'), ('green', 'Зеленая'), ('yellow', 'Желтая'), ('blue', 'Синяя')], max_length=12, verbose_name='Цвет')),
                ('coordinates', models.ManyToManyField(to='address.coordinate')),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.hub', verbose_name='Хаб')),
            ],
            options={
                'verbose_name': 'Зона хаба',
                'verbose_name_plural': 'Зоны хабов',
                'db_table': 'hub_zone',
            },
        ),
        migrations.CreateModel(
            name='GlobalAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256, null=True, verbose_name='адрес')),
                ('city', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город')),
                ('coordinate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate', verbose_name='Координаты')),
            ],
            options={
                'verbose_name': 'Глобальный адрес',
                'verbose_name_plural': 'Глобальные адреса',
                'db_table': 'address_globaladdress',
            },
        ),
        migrations.AddConstraint(
            model_name='coordinate',
            constraint=models.UniqueConstraint(fields=('latitude', 'longitude'), name='unique_coords'),
        ),
        migrations.AddField(
            model_name='cityzone',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='cityzone',
            name='coordinates',
            field=models.ManyToManyField(to='address.coordinate'),
        ),
        migrations.AddField(
            model_name='city',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='address',
            name='coordinate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.coordinate', verbose_name='Координаты'),
        ),
    ]
