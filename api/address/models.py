from tabnanny import verbose
from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from slugify import slugify
from shapely import geometry

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
    zone = models.ManyToManyField(
        "Coordinate", verbose_name=_('координаты'),
        blank=True, related_name="zone"
    )

    objects = models.Manager()

    class Meta:
        db_table = "address_city"
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self) -> str:
        return f"{self.country}, {self.region}, {self.city}"

    def save(self, *args, **kwargs):
        if not self.center:
            self.center = self._get_center_from_request()

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
    
    def zone_as_list(self):
        return self.zone.values_list("latitude", "longitude")
    
    def coords_in_zone(self, coords):
        coords_point = geometry.Point(
            coords.latitude,
            coords.longitude
        )

        zone_polygon = geometry.Polygon(
            self.zone_as_list()
        )

        return zone_polygon.contains(coords_point)

class AbstractAddressModel(models.Model):
    coordinate = models.ForeignKey(
        "Coordinate", models.CASCADE,
        verbose_name=_('Координаты'),
        null=True, blank=True,
    )

    objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.pk)


class Address(AbstractAddressModel):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        blank=True, default=None,
    )
    street = models.CharField(
        _('Улица'), max_length=128,
        null=True, blank=True
    )
    number = models.CharField(
        _('Номер дома'), max_length=12,
        null=True, blank=True
    )
    address = models.CharField(
        _('Сырые данные'), max_length=256,
        null=True, blank=True
    )
    address_lower = models.CharField(
        _('Сырые данные lower'), max_length=256,
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
        self.address = self.model_as_raw()
        self.address_lower = self.address.lower()

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

    def model_as_raw(self, region=True):
        return f"{self.city.region}, {self.city.city}, {self.street}, {self.number}"


class Hub(AbstractAddressModel):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('Город'),
        blank=True, default=None,
    )
    title = models.CharField(
        _('Название'), max_length=256,
        unique=True
    )
    title_lower = models.CharField(
        _('Название lower'), max_length=256,
        null=True, blank=True
    )
    slug = models.SlugField(
        _('Слаг'), default="",
        blank=True, null=True
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
        self.slug = self.create_slug()
        self.title_lower = self.title.lower()

        super().save(*args, **kwargs)

        return self

    def create_slug(self):
        return slugify(self.title)

    def get_coords_as_string(self):
        return self.coordinate.get_string()


class GlobalAddress(AbstractAddressModel):
    address = models.CharField(
        _('адрес'), max_length=256, unique=True
    )
    address_lower = models.CharField(
        _('Адрес lower'), max_length=256,
        null=True, blank=True
    )

    class Meta:
        db_table = "address_globaladdress"
        verbose_name = "Глобальный адрес"
        verbose_name_plural = "Глобальные адреса"

    def __str__(self):
        return str(self.address)
    
    def save(self, *args, **kwargs):
        self.address_lower = self.address.lower()

        super().save(*args, **kwargs)


class Coordinate(models.Model):
    latitude = models.FloatField(
        _('Широта')
    )
    longitude = models.FloatField(
        _('Долгота')
    )

    objects = models.Manager()

    class Meta:
        db_table = "city_zone_coordinate"
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"

    def __str__(self) -> str:
        return f"{self.latitude}, {self.longitude}"

    def get_tuple(self):
        return (self.latitude, self.longitude)
    
    def get_string(self):
        return f"{self.latitude}, {self.longitude}"


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

    objects = models.Manager()

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
    title: str = models.CharField(
        _('Название'), max_length=256, default=""
    )
    color: str = models.CharField(
        verbose_name=_('Цвет'), choices=ZONE_COLORS, max_length=12
    )
    coordinates: List[Coordinate] = models.ManyToManyField(
        Coordinate,
    )

    objects = models.Manager()

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

        return self

    def get_coordinates_as_list(self):
        coords = []

        for coord in self.coordinates.all():
            coords.append([coord.latitude, coord.longitude])

        return coords


class CitySearchSelect:
    regions = set(City.objects.values_list('region', flat=True))
    cities = {
        region: set(City.objects.filter(
            region=region
        ).values_list("city", flat=True))
        for region in regions
    }

    @staticmethod
    def update():
        CitySearchSelect.regions = set(City.objects.values_list('region', flat=True))
        CitySearchSelect.cities = {
            region: set(City.objects.filter(
                region=region
            ).values_list("city", flat=True))
            for region in CitySearchSelect.regions
        }


@receiver([post_save, post_delete], sender=City)
def new_city_reciver(sender, instance, **kwargs):
    CitySearchSelect.update()
