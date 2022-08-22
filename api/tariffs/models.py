from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import CityZone, City
from api.cars.models import CAR_CLASSES
from api.exceptions import TariffNotSpecifiedException


TARIFF_TYPE = (
    ("default", "Стандартный"),
    ("contract", "Договор")
)


class PriceToCarClass(models.Model):
    car_class = models.CharField(
        _('Класс автомобиля'), choices=CAR_CLASSES, max_length=32
    )
    customer_price = models.IntegerField(
        _('Цена заказчика'), default=0
    )
    driver_price = models.IntegerField(
        _('Цена водителя'), default=0
    )

    class Meta:
        db_table = "car_zone_price2car_class"
        verbose_name = "Цена к классу авто"
        verbose_name_plural = "Цены к классам авто"
    
    def __str__(self) -> str:
        return f"{self.car_class} - ({self.customer_price} , {self.driver_price})"


class ZoneToPrice(models.Model):
    zone = models.ForeignKey(
        CityZone, models.CASCADE,
        verbose_name=_('Зона')
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Цены к зоне'),
    )

    class Meta:
        db_table = "zone_to_prices"
        verbose_name = "Зона к ценам"
        verbose_name_plural = "Зоны к ценам"

    def __str__(self) -> str:
        return f"{self.zone}"


class ServiceToPrice(models.Model):
    service = models.CharField(
        _('Услуга'), max_length=128,
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Услуга к цене')
    )

    class Meta:
        db_table = "service_to_price"
        verbose_name = "Услуга к ценам"
        verbose_name_plural = "Услуги к ценам"

    def __str__(self) -> str:
        return f"{self.service}"


class IntracityTariff(models.Model):
    name = models.CharField(
        _('Название'), max_length=128
    )
    type = models.CharField(
        _('Тип тарифа'), choices=TARIFF_TYPE,
        max_length=16, default="default"
    )
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        null=True, blank=True
    )
    zone_prices = models.ManyToManyField(
        ZoneToPrice, verbose_name=_('Цены к зонам')
    )
    service_prices = models.ManyToManyField(
        ServiceToPrice, verbose_name=_('Цены к услугам')
    )

    class Meta:
        db_table = "intracity_tariff"
        verbose_name = "Внутригородской тариф"
        verbose_name_plural = "Внутригородские тарифы"
    
    def __str__(self) -> str:
        return f"{self.name}"


class IntercityTariff(models.Model):
    distance = models.IntegerField(
        _('Расстояние')
    )
    from_city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Из грода'),
        related_name=_("from_city")
    )
    to_city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('В город'),
        related_name=_('to_city')
    )
    service_prices = models.ManyToManyField(
        ServiceToPrice, verbose_name=_('Цены к услугам')
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Услуга к цене')
    )

    class Meta:
        db_table = "intercity_tariff"
        verbose_name = "Межгородской тариф"
        verbose_name_plural = "Межгородские тарифы"

    def __str__(self) -> str:
        return f"{self.from_city.city} -> {self.to_city.city}"


class Tariff(models.Model):
    intracity_tariff = models.ForeignKey(
        IntracityTariff, models.CASCADE,
        verbose_name=_('Внутригородской тариф'),
        null=True, blank=True
    )
    intercity_tariff = models.ForeignKey(
        IntercityTariff, models.CASCADE,
        verbose_name=_('межгородской тариф'),
        null=True, blank=True
    )

    class Meta:
        db_table = "tariff"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self) -> str:
        return self.tariff

    @property
    def tariff(self):
        if self.intercity_tariff_id is not None:
            return self.intercity_tariff
        if self.intracity_tariff_id is not None:
            return self.intracity_tariff

        raise TariffNotSpecifiedException(
            "Не указан междугородской или внутригородской тариф"
        )