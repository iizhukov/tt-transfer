from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.address.models import Address, City
from api.profile.models import Company, Manager
from api.tariffs.models import IntracityTariff, IntercityTariff
from api.cars.models import CAR_CLASSES


def claculate_price():
    return 0


class OrderDetailModel(models.Model):
    contractor = models.ForeignKey(
        Company, models.CASCADE, verbose_name=_('Заказчик'),
        null=True
    )
    datetime = models.DateTimeField(
        _('Дата и время заказа'), default=timezone.now
    )
    manager = models.ForeignKey(
        Manager, models.CASCADE, verbose_name=_('Менеджер')
    )
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
    )
    car_class = models.CharField(
        _('Класс авто'), choices=CAR_CLASSES, max_length=32
    )

    intercity_tariff = models.ForeignKey(
        IntercityTariff, models.CASCADE, verbose_name=_('Межгородской тариф тариф'),
        null=True, blank=True, default=None
    )
    intracity_tariff = models.ForeignKey(
        IntracityTariff, models.CASCADE, verbose_name=_('Внутригородской тариф'),
        null=True, blank=True, default=None
    )

    class Meta:
        db_table = "order_detail"
        verbose_name = "Детали заказа"
        verbose_name_plural = "Детали заказов"

    def __str__(self) -> str:
        return f""


class Order(models.Model):
    from_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Из'),
        related_name="from+",
    )
    to_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('В'),
        related_name="to"
    )
    
    car_class = models.CharField(
        _('Класс автомобиля'), choices=CAR_CLASSES, max_length=24,
    )

    client_name = models.CharField(
        _('Имя клиента'), max_length=64, blank=True, null=True,
    )
    client_surname = models.CharField(
        _('Фамилия клиента'), max_length=64, blank=True, null=True,
    )
    client_patronymic = models.CharField(
        _('Отчество клиента'), max_length=64, blank=True, null=True,
    )
    clinet_phone = models.CharField(
        _('Телефон клиента'), max_length=14, blank=True, null=True,
    )

    # manager = models.ForeignKey()

    date = models.DateField(
        _('Дата заказа'), default=timezone.now
    )
    time = models.TimeField(
        _('Время заказа'), default=timezone.now
    )
    price = models.IntegerField(
        _('Цена'), blank=True, default=None
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"{self.contractor}"

    def save(self, *args, **kwargs) -> None:
        self.price = self._calculate_price()

        return super().save(args, kwargs)

    def _calculate_price(self):
        return 0