# Generated by Django 4.0.6 on 2022-09-05 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=64, verbose_name='Марка')),
                ('model', models.CharField(max_length=128, verbose_name='Модель')),
                ('license_plate', models.CharField(max_length=10, verbose_name='Номер')),
                ('power', models.IntegerField(verbose_name='Мощность')),
                ('engine_capacity', models.FloatField(verbose_name='Объем двигателя')),
                ('color', models.CharField(max_length=32, verbose_name='Цвет')),
                ('sts', models.CharField(max_length=10, verbose_name='СТС')),
                ('pts', models.CharField(max_length=15, verbose_name='ПТС')),
                ('car_class', models.CharField(choices=[('standart', 'Стандарт'), ('comfort', 'Комфорт'), ('minivan', 'Минивен'), ('business', 'Бизнес'), ('representative', 'Представительский'), ('suv', 'SUV'), ('minibus', 'Микроавтобус'), ('minivan_business', 'Минивен Бизнес'), ('minibus_business', 'Микроавтобус Бизнес'), ('bus30', 'Автобус 30+'), ('bus43', 'Автобус 43+'), ('bus50', 'Автобус 50+')], max_length=24, verbose_name='Класс')),
                ('status', models.CharField(choices=[('main', 'Основной'), ('spare', 'Запасной')], default='spare', max_length=12, verbose_name='Статус автомобиля')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
                'db_table': 'car',
            },
        ),
    ]
