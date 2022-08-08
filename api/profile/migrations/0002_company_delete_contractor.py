# Generated by Django 4.0.6 on 2022-07-28 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0002_alter_address_options'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('financial_turnover', models.IntegerField(default=0, verbose_name='Финансовый оборот')),
                ('status', models.CharField(choices=[('constant', 'Постоянный'), ('default', 'Обычный')], default='default', max_length=12, verbose_name='Статус')),
                ('gen_director_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя Ген директора')),
                ('gen_director_surname', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия Ген директора')),
                ('gen_director_patronymic', models.CharField(blank=True, max_length=64, null=True, verbose_name='Отчество Ген директора')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.address', verbose_name='Адрес')),
                ('responsible', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
                'db_table': 'company',
            },
        ),
        migrations.DeleteModel(
            name='Contractor',
        ),
    ]
