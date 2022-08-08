# Generated by Django 4.0.6 on 2022-08-04 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricetocarclass',
            options={'verbose_name': 'Цена к классу авто', 'verbose_name_plural': 'Цены к классам авто'},
        ),
        migrations.AlterField(
            model_name='pricetocarclass',
            name='car_class',
            field=models.CharField(choices=[('business', 'Бизнес'), ('standart', 'Стандарт'), ('representative', 'Представительский'), ('minivan', 'Минивен'), ('minibus', 'Микроавтобус'), ('comfort', 'Комфорт'), ('bus', 'Автобус'), ('business_plus', 'Бизнес плюс'), ('cargo', 'Грузовой')], max_length=32, verbose_name='Класс автомобиля'),
        ),
    ]
