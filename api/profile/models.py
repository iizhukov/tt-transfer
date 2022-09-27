from traceback import format_exc
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import Address, City
from api.cars.models import Car


STATUSES = (
    ('constant', 'Постоянный'),
    ('default', 'Обычный')
)


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


class EmployeeModel(models.Model):
    user = models.OneToOneField(
        "authentication.User", models.CASCADE, verbose_name=_('Пользователь')
    )

    class Meta:
        db_table = "employee"
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

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
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        null=True, blank=True
    )
    passport = models.CharField(
        _('Паспорт'), max_length=10, blank=True, null=True,
    )
    driving_license = models.CharField(
        verbose_name=_('Водительское удостоверение'), max_length=10,
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


class BankModel(models.Model):
    name = models.CharField(
        _('Название'), max_length=128
    )
    bic = models.CharField(
        _('БИК'), max_length=9
    )

    class Meta:
        db_table = "bank"
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

    def __str__(self) -> str:
        return str(self.name)


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

    owner = models.ForeignKey(
        "authentication.User", models.CASCADE, verbose_name=_('Ответственный'),
        null=True, blank=True
    )
    employees = models.ManyToManyField(
        EmployeeModel, blank=True
    )

    tin = models.CharField(
        _('ИНН'), max_length=12,
        default=""
    )
    rrc = models.CharField(
        _('КПП'), max_length=9,
        null=True, blank=True
    )

    bank = models.ForeignKey(
        BankModel, models.PROTECT,
        verbose_name=_('Банк'), null=True,
        blank=True
    )
    checking_account = models.CharField(
        _('Расчетный счет'), max_length=20,
        default=""
    )
    corporate_account = models.CharField(
        _('Корпоративный счет'), max_length=20,
        default=""
    )

    confirmed = models.BooleanField(
        _('Подтвержден'), default=False,
    )


    class Meta:
        db_table = 'company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self) -> str:
        return f"{self.name} - {self.address}"
