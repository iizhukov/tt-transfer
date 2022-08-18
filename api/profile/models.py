from django.db import models
from django.utils.translation import gettext_lazy as _

from api.authentication.models import User
from api.address.models import Address


STATUSES = (
    ('constant', 'Постоянный'),
    ('default', 'Обычный')
)


class Client(models.Model):
    user = models.OneToOneField(
        User, models.CASCADE, verbose_name=_('Пользователь')
    )
    status = models.CharField(
        _('Статус'), choices=STATUSES, max_length=12,
        default='default'
    )
    financial_turnover = models.IntegerField(
        _('Финансовый оборот'), default=0,
    )
    locality = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Адрес')
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
    location = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Адрес')
    )
    user = models.OneToOneField(
        User, models.CASCADE, verbose_name=_('Ответственный')
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

    class Meta:
        db_table = 'company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self) -> str:
        return f"{self.name} - {self.financial_turnover}"


class Manager(models.Model):
    user = models.OneToOneField(
        User, models.CASCADE, verbose_name=_('Пользователь')
    )

    class Meta:
        db_table = "manager"
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self) -> str:
        return f"{self.user}"
