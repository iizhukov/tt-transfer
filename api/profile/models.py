from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import Address, City
from api.cars.models import Car


STATUSES = (
    ('constant', 'Постоянный'),
    ('default', 'Обычный')
)


class Client(models.Model):
    user = models.OneToOneField(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь')
    )
    status = models.CharField(
        _('Статус'), choices=STATUSES, max_length=12,
        default='default'
    )
    financial_turnover = models.IntegerField(
        _('Финансовый оборот'), default=0,
    )

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    
    def __str__(self) -> str:
        return f"{self.user.name} {self.user.surname} - {self.financial_turnover} р."


class Company(models.Model):
    name = models.CharField(
        _('Название'), max_length=128
    )
    address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Адрес'),
        null=True, blank=True
    )
    user = models.ForeignKey(
        "authentication.User", models.CASCADE, verbose_name=_('Ответственный'),
        null=True, blank=True
    )
    financial_turnover = models.IntegerField(
        _('Финансовый оборот'), default=0,
    )
    status = models.CharField(
        _('Статус'), choices=STATUSES, max_length=12,
        default='default'
    )

    gen_director_name = models.CharField(
        _('Имя Ген директора'), max_length=64,
        blank=True, null=True,
    )
    gen_director_surname = models.CharField(
        _('Фамилия Ген директора'), max_length=64,
        blank=True, null=True,
    )
    gen_director_patronymic = models.CharField(
        _('Отчество Ген директора'), max_length=64,
        blank=True, null=True,
    )

    confirmed = models.BooleanField(
        _('Подтвержден'), default=False,
    )

    class Meta:
        db_table = 'company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self) -> str:
        return f"{self.name} - {self.financial_turnover}"


class Manager(models.Model):
    user = models.OneToOneField(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь')
    )

    class Meta:
        db_table = "manager"
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self) -> str:
        return f"{self.user}"


class Admin(models.Model):
    user = models.OneToOneField(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь')
    )

    class Meta:
        db_table = "admin"
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self) -> str:
        return f"{self.user}"


class Driver(models.Model):
    STATUSES = (
        ('free', 'Свободен'),
        ('busy', 'Занят')
    )

    user = models.OneToOneField(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь')
    )
    car = models.OneToOneField(
        Car, models.CASCADE, verbose_name=_('Автомобиль'),
        null=True, blank=True
    )
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        null=True, blank=True
    )
    driving_license = models.CharField(
        verbose_name=_('Права'), max_length=10,
        null=True, blank=True
    )
    status = models.CharField(
        _('Статус'), choices=STATUSES, max_length=12,
        default="busy"
    )

    class Meta:
        db_table = "driver"
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self) -> str:
        return f"{self.user}"
