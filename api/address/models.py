from typing import List
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
        self.center = self._get_center_from_request()
        print("save")

        if "(" in self.city:
            self.city = self.city.split("(")[0].rstrip()

        return super().save(*args, **kwargs)

    def _get_center_from_request(self):
        latitude, longitude = GetCoordsByAddress.get(
            self.__str__()
        )

        if longitude and latitude:
            return Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )[0]

        return None

    def get_center_as_string(self):
        return f"{self.center.latitude}, {self.center.longitude}"


class AbstractAddressModel(models.Model):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        blank=True, default=None,
    )
    coordinate = models.ForeignKey(
        "Coordinate", models.CASCADE,
        verbose_name=_('Координаты'),
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.model_as_raw()

    def model_as_raw(self, region=True):
        return f"{self.city}, {self.street}, {self.number}"


class Address(AbstractAddressModel):
    street = models.CharField(
        _('Улица'), max_length=128,
        null=True, blank=True
    )
    number = models.CharField(
        _('Номер дома'), max_length=12,
        null=True, blank=True
    )

    class Meta:
        db_table = "address"
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
    
    def __str__(self) -> str:
        return self.model_as_raw()


    def save(self, *args, **kwargs):
        self.coordinate = self._get_coords_from_request()

        return super().save(*args, **kwargs)

    def _get_coords_from_request(self):
        latitude, longitude = GetCoordsByAddress.get(
            self.model_as_raw()
        )

        if longitude and latitude:
            return Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )[0]

        return None


class Hub(AbstractAddressModel):
    title = models.CharField(
        _('Название'), max_length=256,
    )
    description = models.TextField(
        _('Описание'), null=True, blank=True
    )

    class Meta:
        db_table = "address_hub"
        verbose_name = "Хаб"
        verbose_name_plural = "Хабы"

    def __str__(self) -> str:
        return f"{self.pk}: {self.city.city}, {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        return self


class GlobalAddress(AbstractAddressModel):
    address = models.CharField(
        _('адрес'), max_length=256, null=True
    )

    class Meta:
        db_table = "address_globaladdress"
        verbose_name = "Глобальный адрес"
        verbose_name_plural = "Глобальные адреса"


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


class HubZone(models.Model):
    hub: Hub = models.ForeignKey(
        Hub, models.CASCADE, verbose_name=_('Хаб')
    )
    color: str = models.CharField(
        verbose_name=_('Цвет'), choices=ZONE_COLORS, max_length=12
    )
    coordinates: List[Coordinate] = models.ManyToManyField(
        Coordinate,
    )

    class Meta:
        db_table = "hub_zone"
        verbose_name = "Зона хаба"
        verbose_name_plural = "Зоны хабов"

    def __str__(self) -> str:
        return f"{self.pk}: {self.hub.title}, {self.color}"

    def save(self, coordinates=None, *args, **kwargs) -> None:
        super().save(args, kwargs)

        if coordinates:
            self.coordinates.clear()

            for latitude, longitude in coordinates:
                self.coordinates.add(
                    Coordinate.objects.get_or_create(
                        latitude=latitude,
                        longitude=longitude
                    )[0]
                )

    def get_coordinates_as_list(self):
        coords = []

        for coord in self.coordinates.all():
            coords.append([coord.latitude, coord.longitude])

        return coords
