from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from api.address.models import CityZone, City, HubZone, Hub, GlobalAddress
from api.cars.models import CAR_CLASSES
from api.exceptions import TariffNotSpecifiedException
from api.request import DistanceAndDuration


def tariff_derault_timelife():
    return timezone.now() + timezone.timedelta(days=365)


def set_default_car_classes_price(customer_price=0):
    prices = []

    for car_class in CAR_CLASSES:
        price = PriceToCarClass.objects.create(
            car_class=car_class[0],
            customer_price=customer_price
        )
        prices.append(price)

    return prices


def add_hub_to_tariffs(hub: Hub):
    city = hub.city

    tariffs: List[Tariff] = Tariff.objects.filter(city=city)
    hub_to_price = HubToPrice.objects.filter(
        hub=hub
    ).first()

    for tariff in tariffs:
        if hub_to_price not in tariff.intracity_tariff.hub_to_prices:
            tariff.intracity_tariff.hub_to_prices.add(
                hub_to_price
            )


DEFAULT_SERVICES_LIST = (
    ("Аренда по времени (руб./час)", "rent_by_time"),
    ("Аренда по расстоянию (руб./км)", "rent_by_distance"),
    ("Дополнительные заезд (руб)", "addtional_check_in"),
    ("Ожидание (руб)", "expectation"),
)
DEFAULT_SERVICES_ONLY_DRIVERS_LIST = (
    ("Минимальный заказ (час)", "minimal_order"),
)


class PriceToCarClass(models.Model):
    car_class = models.CharField(
        verbose_name=_('Класс авто'), choices=CAR_CLASSES, max_length=64
    )
    customer_price = models.IntegerField(
        _('Цена заказчика'), default=None,
        null=True, blank=True
    )
    driver_price = models.IntegerField(
        _('Цена водителя'), default=0
    )

    class Meta:
        db_table = "car_zone_price2car_class"
        verbose_name = "Цена к классу авто"
        verbose_name_plural = "Цены к классам авто"
    
    def __str__(self) -> str:
        return f"{self.pk}: {self.car_class} - ({self.customer_price} , {self.driver_price})"


class ServiceToPrice(models.Model):
    title = models.CharField(
        _('Название'), max_length=128,
        default=""
    )
    slug = models.CharField(
        _('Тип'), max_length=128,
        default=""
    )
    prices: PriceToCarClass = models.ManyToManyField(
        PriceToCarClass, verbose_name=_('Услуга к цене'),
        blank=True
    )

    class Meta:
        db_table = "service_to_price"
        verbose_name = "Услуга к ценам"
        verbose_name_plural = "Услуги к ценам"

    def __str__(self) -> str:
        return f"{self.pk}: {self.title} - {self.slug}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self._add_prices_to_service()

        return self

    def delete(self, *args, **kwargs):
        for price in self.prices:
            self.prices.remove(price)

            price.delete()
    
        return super().delete(*args, **kwargs)

    def _add_prices_to_service(self):
        customer_price = 0

        if self.slug in DEFAULT_SERVICES_ONLY_DRIVERS_LIST:
            customer_price = None

        self.prices.add(*set_default_car_classes_price(customer_price))


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self._set_prices_to_zone()

        return self

    def delete(self, *args, **kwargs):
        for price in self.prices:
            self.prices.remove(price)

            price.delete()
    
        return super().delete(*args, **kwargs)

    def _set_prices_to_zone(self):
        self.prices.add(*set_default_car_classes_price())


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self._set_prices()
        self._add_addtional_hub_zones_price()

        return self

    def delete(self, *args, **kwargs):
        for price in self.prices:
            self.prices.remove(price)

            price.delete()
    
        return super().delete(*args, **kwargs)

    def _set_prices(self):
        self.prices.add(*set_default_car_classes_price())

    def _add_addtional_hub_zones_price(self, hubzones=None):
        if not hubzones:
            hubzones = HubZone.objects.filter(
                hub=self.hub
            )

        for zone in hubzones:
            self.additional_hubzone_prices.add(
                AdditionalHubZoneToPrice.objects.create(
                    zone=zone
                )
            )


class IntracityTariff(models.Model):
    hub_to_prices: List[HubToPrice] = models.ManyToManyField(
        HubToPrice, verbose_name=_('Цены к зонам')
    )

    class Meta:
        db_table = "intracity_tariff"
        verbose_name = "Внутригородской тариф"
        verbose_name_plural = "Внутригородские тарифы"
    
    def __str__(self) -> str:
        return f"{self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        return self

    def delete(self, *args, **kwargs):
        for htp in self.hub_to_prices:
            self.hub_to_prices.remove(htp)

        self.save()

        return super().delete(*args, **kwargs)


class AbstractLocationToPrice(models.Model):
    distance = models.FloatField(
        _('Расстояние'), default=-1
    )
    hours_duration = models.IntegerField(
        _('Часы'), default=-1
    )
    minutes_duration = models.IntegerField(
        _('Минуты'), default=-1
    )
    prices = models.ManyToManyField(
        PriceToCarClass, blank=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        set_prices = False

        if not self.pk:
            set_prices = True

        super().save(*args, **kwargs)

        if set_prices:
            self._set_prices()

        return self

    def delete(self, *args, **kwargs):
        for price in self.prices:
            self.prices.remove(price)

            price.delete()
    
        return super().delete(*args, **kwargs)

    def _set_prices(self):
        self.prices.add(*set_default_car_classes_price())


class CityToPrice(AbstractLocationToPrice):
    city = models.ForeignKey(
        City, models.CASCADE, verbose_name=_('В город')
    )

    class Meta:
        db_table = "city_to_price"
        verbose_name = "Город к ценам"
        verbose_name_plural = "Города к ценам"

    def __str__(self) -> str:
        return f"{self.pk}: {self.city}"


class GlobalAddressToPrice(AbstractLocationToPrice):
    global_address = models.ForeignKey(
        GlobalAddress, models.CASCADE, verbose_name=_('В глобальный адрес')
    )

    class Meta:
        db_table = "global_address_to_price"
        verbose_name = "Глобальный адрес к ценам"
        verbose_name_plural = "Глобальные адреса к ценам"

    def __str__(self) -> str:
        return f"{self.pk}: {self.global_address}"


class IntercityTariff(models.Model):
    cities = models.ManyToManyField(
        CityToPrice, verbose_name=_('В города'),
        blank=True
    )
    global_addresses = models.ManyToManyField(
        GlobalAddressToPrice, verbose_name=_('В глобальные адреса'),
        blank=True
    )

    class Meta:
        db_table = "intercity_tariff"
        verbose_name = "Межгородской тариф"
        verbose_name_plural = "Межгородские тарифы"

    def __str__(self) -> str:
        return f"{self.pk}"


class Tariff(models.Model):
    CURRENCIES = (
        ('rub', 'Рубль'),
        ('eur', 'Евро'),
        ('usd', 'Доллар'),
        ('cny', 'Юани'),
    )

    title = models.CharField(
        _('Название'), max_length=128, 
        null=True, blank=True
    )
    city: City = models.ForeignKey(
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
    services: ServiceToPrice = models.ManyToManyField(
        ServiceToPrice, verbose_name=_('Цены к услугам'),
        blank=True
    )
    intracity_tariff: IntracityTariff = models.OneToOneField(
        IntracityTariff, on_delete=models.CASCADE,
        verbose_name=_('Внутригородской тариф'),
        null=True, blank=True
    )
    intercity_tariff: IntercityTariff = models.OneToOneField(
        IntercityTariff, on_delete=models.CASCADE,
        verbose_name=_('Межгородской тариф'),
        null=True, blank=True
    )

    is_commission = models.BooleanField(
        _('Комиссионный?'), default=False
    )
    lifetime = models.DateTimeField(
        _('Срок жизни'), default=tariff_derault_timelife
    )

    class Meta:
        db_table = "tariff"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self) -> str:
        return f"{self.pk}: {self.city.city}, {self.title}, Комиссионный: {self.is_commission}"

    def save(self, *args, **kwargs):
        self._set_intercity_tariff()
        self._set_hub_prices()

        super().save(*args, **kwargs)

        self._set_default_services()

        return self

    def delete(self, *args, **kwargs):
    
        return super().delete(*args, **kwargs)

    def _set_default_services(self):
        for service in [
            *DEFAULT_SERVICES_LIST,
            *DEFAULT_SERVICES_ONLY_DRIVERS_LIST
            ]:
            service_ = ServiceToPrice.objects.create(
                title=service[0],
                slug=service[1]
            )
            self.services.add(service_)

    def _set_hub_prices(self, hubs=None):
        intracity_tariff = self.intracity_tariff or IntracityTariff.objects.create()
        
        if not hubs:
            hubs = Hub.objects.filter(
                city=self.city
            )

        print(hubs)

        for hub in hubs:
            hub_to_price = HubToPrice.objects.create(
                hub=hub
            )
            intracity_tariff.hub_to_prices.add(hub_to_price)
        
        self.intracity_tariff = intracity_tariff

    def _set_intercity_tariff(self):
        self.intercity_tariff = IntercityTariff.objects.create()


@receiver(m2m_changed, sender=IntercityTariff.cities.through)
def func(sender, instance, **kwargs):
    if kwargs.get("action", "pre_add") == "pre_add":
        return

    tariff_city: City = instance.tariff.city
    city_to_price: CityToPrice = CityToPrice.objects.get(
        id=kwargs.get("pk_set").pop()
    )

    res = DistanceAndDuration.get(
        tariff_city.get_center_as_string(),
        city_to_price.city.get_center_as_string()
    )

    print(res)

    city_to_price.distance = res[0]
    city_to_price.hours_duration = res[1]
    city_to_price.minutes_duration = res[2]

    city_to_price.save()
