from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.db.models.constraints import UniqueConstraint

from api.cars.models import CAR_CLASSES
from api.request import GetCoordsByAddress


ZONE_COLORS = (
    ('red', 'Красная'),
    ('green', 'Зеленая'),
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

    center = models.ForeignKey(
        "Coordinate", models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        db_table = "address_city"
        verbose_name = "Город"
        verbose_name_plural = "Города"
    
    def __str__(self) -> str:
        return f"{self.country}, {self.region}, {self.city}"

    def save(self, *args, **kwargs):
        latitude, longitude = GetCoordsByAddress.get(
            self.__str__()
        )

        if longitude and latitude:
            self.center = Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )[0]
        else:
            self.center = None

        return super().save(args, kwargs)


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
    coordinate = models.ForeignKey(
        "Coordinate", models.CASCADE,
        verbose_name=_('Координаты'),
        null=True, blank=True,
    )

    class Meta:
        db_table = "address"
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
    
    def __str__(self) -> str:
        return self.model_as_raw()

    def model_as_raw(self, region=True):
        return f"{self.city}, {self.street}, {self.number}"

    def save(self, *args, **kwargs):
        latitude, longitude = GetCoordsByAddress.get(
            self.model_as_raw()
        )

        if longitude and latitude:
            self.coordinate = Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )[0]
        else:
            self.coordinate = None

        return super().save(args, kwargs)


class Coordinate(models.Model):
    latitude = models.FloatField(
        _('Широта')
    )
    longitude = models.FloatField(
        _('Долгота')
    )

    class Meta:
        db_table = "city_zone_coordinate"
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"
        constraints = [
            UniqueConstraint(
                fields=('latitude', 'longitude'),
                name="unique_coords"
            )
        ]

    def __str__(self) -> str:
        return f"{self.latitude}, {self.longitude}"

    def get_tuple(self):
        return (self.latitude, self.longitude)


class CityZone(models.Model):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
    )
    color = models.CharField(
        verbose_name=_('Цвет'), choices=ZONE_COLORS, max_length=12
    )
    coordinates = models.ManyToManyField(
        Coordinate,
    )

    class Meta:
        db_table = "city_zone"
        verbose_name = "Зона города"
        verbose_name_plural = "Зоны городов"

    def __str__(self) -> str:
        return f"{self.pk}: {self.city.city}, {self.color}"

    def get_coordinates_as_list(self):
        coords = []

        for coord in self.coordinates.all():
            coords.append([coord.latitude, coord.longitude])

        return coords
