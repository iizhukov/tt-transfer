from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import CityZone, City, HubZone, Hub
from api.cars.models import CAR_CLASSES
from api.exceptions import TariffNotSpecifiedException


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


class AdditionalHubZoneToPrice(models.Model):
    zone = models.ForeignKey(
        HubZone, models.CASCADE,
        verbose_name=_('Зона')
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Цены к зоне'),
    )

    class Meta:
        db_table = "additional_hubzone_to_price"
        verbose_name = "Зона хаба к ценам"
        verbose_name_plural = "Зоны хаба к ценам"

    def __str__(self) -> str:
        return f"{self.zone}"


class HubToPrice(models.Model):
    hub: Hub = models.ForeignKey(
        Hub, models.CASCADE, verbose_name=_('Хаб')
    )
    prices = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Цены к классу авто')
    )
    additional_hubzone_prices = models.ManyToManyField(
        AdditionalHubZoneToPrice, verbose_name=_('Добавочная стоимость к зонам хаба')
    )

    class Meta:
        db_table = "hub_to_price"
        verbose_name = "Хаб к ценам"
        verbose_name_plural = "Хабы у ценам"

    def __str__(self) -> str:
        return f"{self.hub.title}"


class IntracityTariff(models.Model):
    service_prices = models.ManyToManyField(
        ServiceToPrice, verbose_name=_('Цены к услугам')
    )
    hub_to_prices = models.ManyToManyField(
        HubToPrice, verbose_name=_('Цены к зонам')
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
    CURRENCIES = (
        ('rub', 'Рубль'),
        ('eur', 'Евро'),
        ('usd', 'Доллар'),
        ('cny', 'Юани'),
    )

    name = models.CharField(
        _('Название'), max_length=128,
        null=True, blank=True
    )
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        null=True, blank=True
    )
    currency = models.CharField(
        _('валюта'), choices=CURRENCIES,
        default="rub", max_length=5
    )
    comments = models.TextField(
        _('Комментарии'), null=True, blank=True
    )
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

    is_commission = models.BooleanField(
        _('Комиссионный?'), default=False
    )

    class Meta:
        db_table = "tariff"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self) -> str:
        return f"{self.city.city}: {self.name}, Комиссионный-{self.is_commission}"
