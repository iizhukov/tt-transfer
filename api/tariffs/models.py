from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import CityZone
from api.cars.models import CAR_CLASSES


class PriceToCarClass(models.Model):
    car_class = models.CharField(
        _('Класс автомобиля'), choices=CAR_CLASSES, max_length=32
    )
    price = models.IntegerField(
        _('Цена')
    )

    class Meta:
        db_table = "car_zone_price2car_class"
        verbose_name = "Цена к классу авто"
        verbose_name_plural = "Цены к классам авто"
    
    def __str__(self) -> str:
        return f"{self.car_class} - {self.price}"


class IntracityTariff(models.Model):
    name = models.CharField(
        _('Название'), max_length=128
    )
    zone = models.ForeignKey(
        CityZone, models.CASCADE,
        blank=True
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Цена к классу авто')
    )

    class Meta:
        db_table = "intracity_tariff"
        verbose_name = "Внутригородской тариф"
        verbose_name_plural = "Внутригородские тарифы"
    
    def __str__(self) -> str:
        return f"{self.name}"


# class IntercityTariff(models.Model):
#     distance = models.IntegerField(
#         _('Расстояние')
#     )
    


