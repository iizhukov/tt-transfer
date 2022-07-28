from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from api.cars.models import CAR_CLASSES


ZONE_COLORS = (
    ('red', 'Красная'),
    ('green', 'Оранжевая'),
    ('yellow', 'Желтая'),
    ('blue', 'Синяя'),
)


class City(models.Model):
    country = models.CharField(
        _('Страна'), max_length=128,
        default="Россия",
    )
    region = models.CharField(
        _('Регион'), max_length=128,
        null=True,
    )
    city = models.CharField(
        _('Город'), max_length=128,
    )

    class Meta:
        db_table = "address_city"
        verbose_name = "Город"
        verbose_name_plural = "Города"
    
    def __str__(self) -> str:
        return f"{self.country}, {self.region}, {self.city}"


class Address(models.Model):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        blank=True, default=None,
    )
    street = models.CharField(
        _('Улица'), max_length=128,
    )
    number = models.CharField(
        _('Номер дома'), max_length=12,
        default="1",
    )

    class Meta:
        db_table = "address"
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
    
    def __str__(self) -> str:
        return self.model_as_raw()

    def model_as_raw(self, region=True):
        return f"{self.city}, {self.street}, {self.number }"


class PriceToCarClass(models.Model):
    car_class = models.CharField(
        _('Класс автомобиля'), choices=CAR_CLASSES, max_length=32
    )
    price = models.IntegerField(
        _('Цена')
    )

    class Meta:
        db_table = "car_zone_price2car_class"
        verbose_name = "Цена к классу"
        verbose_name_plural = "Цены к классам"
    
    def __str__(self) -> str:
        return f"{self.car_class} - {self.price}"


class Coordinate(models.Model):
    latitude = models.FloatField(
        _('Широта')
    )
    longitude = models.FloatField(
        _('Долгота')
    )

    class Meta:
        db_table = "car_zone_coordinate"
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"

    def __str__(self) -> str:
        return f"{self.latitude}, {self.longitude}"


class CityZone(models.Model):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
    )
    color = models.CharField(
        verbose_name=_('Цвет'), choices=ZONE_COLORS, max_length=12
    )
    prices = models.ManyToManyField(
        PriceToCarClass,
    )
    coordinates = models.ManyToManyField(
        Coordinate,
    )

    class Meta:
        db_table = "car_zone"
        verbose_name = "Зона города"
        verbose_name_plural = "Зоны городов"

    def __str__(self) -> str:
        return f"{self.city.city}, {self.color}"
