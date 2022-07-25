from django.db import models
from django.utils.translation import gettext_lazy as _

from api.authentication.models import User
from api.cars.models import Car


STATUSES = (
    ('free', 'Свободен'),
    ('busy', 'Занят')
)


class Driver(models.Model):
    user = models.OneToOneField(
        User, models.CASCADE, verbose_name=_('Пользователь'),
    )
    car = models.OneToOneField(
        Car, models.CASCADE, verbose_name=_('Автомобиль'),
    )
    locality = models.CharField(
        _('Адрес'), max_length=256,
    )
    driving_license = models.CharField(
        verbose_name=_('Права'), max_length=10,
    )
    status = models.CharField(
        _('Статус'), choices=STATUSES, max_length=12,
    )

    class Meta:
        db_table = 'driver'
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self) -> str:
        return f"{self.user.name} {self.user.surname} - {self.car}"
