from django.db import models
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
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
    street = models.CharField(
        _('Улица'), max_length=128,
    )
    number = models.CharField(
        _('Номер дома'), max_length=12,
        default="1",
    )

    class Meta:
        db_table = "address"
    
    def __str__(self) -> str:
        return f"{self.country}"

    def model_as_raw(self, region=True):
        return f"{self.country}, {self.region}, {self.city}, {self.street}, {self.number }"
