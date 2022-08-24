# Generated by Django 4.0.6 on 2022-08-23 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0002_alter_car_car_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='status',
            field=models.CharField(choices=[('main', 'Основной'), ('spare', 'Запасной')], default='busy', max_length=12, verbose_name='Статус автомобиля'),
        ),
        migrations.AddField(
            model_name='car',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
