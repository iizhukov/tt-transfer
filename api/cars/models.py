from django.db import models
from django.utils.translation import gettext_lazy as _

from api.authentication.models import User


# class CarClass(models.Model):
#     name = models.CharField(
#         _("Название"), max_length=64,
#     )

#     class Meta:
#         db_table = "car_class"
#         verbose_name = "Класс автомобиля"
#         verbose_name_plural = "Классы автомобилей"
    
#     def __str__(self) -> str:
#         return str(self.name)


class Car(models.Model):
    brand = models.CharField(
        _("Марка"), max_length=64,
    )
    model = models.CharField(
        _('Модель'), max_length=128,
    )
    license_plate = models.CharField(
        _("Номер"), max_length=10,
    )
    power = models.IntegerField(_('Мощность'))
    engine_capacity = models.FloatField(_('Объем двигателя'))
    color = models.CharField(
        _('Цвет'), max_length=32,
    )
    sts = models.CharField(
        _('СТС'), max_length=10,
    )
    pts = models.CharField(
        _('ПТС'), max_length=15,
    )
    car_class = models.CharField(
        _("Класс"), max_length=64,
    )
    owner = models.ForeignKey(
        User, models.CASCADE, verbose_name=_('Владелец'),
        null=True, blank=True,
    )

    class Meta:
        db_table = "car"
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
    def __str__(self) -> str:
        return f"{self.brand} : {self.model}"
