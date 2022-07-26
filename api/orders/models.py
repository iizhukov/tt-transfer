from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.address.models import Address
from api.profile.models import Contractor
from api.cars.models import CAR_CLASSES


def claculate_price():
    return 0


class Order(models.Model):
    from_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Из'),
        related_name="from+",
    )
    to_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('В'),
        related_name="to"
    )
    contractor = models.ForeignKey(
        Contractor, models.CASCADE, verbose_name=_('Заказчик'),
    )
    car_class = models.CharField(
        _('Класс автомобиля'), choices=CAR_CLASSES, max_length=12,
    )

    client_name = models.CharField(
        _('Имя клиента'), max_length=64,
    )
    client_surname = models.CharField(
        _('Фамилия клиента'), max_length=64,
    )
    client_patronymic = models.CharField(
        _('Отчество клиента'), max_length=64,
    )
    clinet_phone = models.CharField(
        _('Телефон клиента'), max_length=14, blank=True, null=True,
    )

    date = models.DateField(
        _('Дата заказа'), default=timezone.now
    )
    time = models.DateField(
        _('Время заказа'), default=timezone.now
    )
    price = models.IntegerField(
        _('Цена'), default=claculate_price
    )
