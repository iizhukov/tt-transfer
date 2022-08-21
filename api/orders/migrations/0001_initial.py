# Generated by Django 4.0.6 on 2022-08-21 09:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0003_rename_responsible_company_user_manager'),
        ('tariffs', '0006_intercitytariff'),
        ('address', '0016_address_address_hub_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время заказа')),
                ('car_class', models.CharField(choices=[('business', 'Бизнес'), ('standart', 'Стандарт'), ('representative', 'Представительский'), ('minivan', 'Минивен'), ('minibus', 'Микроавтобус'), ('comfort', 'Комфорт'), ('bus', 'Автобус'), ('business_plus', 'Бизнес плюс'), ('cargo', 'Грузовой')], max_length=32, verbose_name='Класс авто')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.city', verbose_name='Город')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.company', verbose_name='Заказчик')),
                ('intercity_tariff', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tariffs.intercitytariff', verbose_name='Межгородской тариф тариф')),
                ('intracity_tariff', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tariffs.intracitytariff', verbose_name='Внутригородской тариф')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.manager', verbose_name='Менеджер')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказов',
                'db_table': 'order_detail',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_class', models.CharField(choices=[('business', 'Бизнес'), ('standart', 'Стандарт'), ('representative', 'Представительский'), ('minivan', 'Минивен'), ('minibus', 'Микроавтобус'), ('comfort', 'Комфорт'), ('bus', 'Автобус'), ('business_plus', 'Бизнес плюс'), ('cargo', 'Грузовой')], max_length=24, verbose_name='Класс автомобиля')),
                ('client_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя клиента')),
                ('client_surname', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия клиента')),
                ('client_patronymic', models.CharField(blank=True, max_length=64, null=True, verbose_name='Отчество клиента')),
                ('clinet_phone', models.CharField(blank=True, max_length=14, null=True, verbose_name='Телефон клиента')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время заказа')),
                ('price', models.IntegerField(blank=True, default=None, verbose_name='Цена')),
                ('from_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from+', to='address.address', verbose_name='Из')),
                ('to_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='address.address', verbose_name='В')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
            },
        ),
    ]
