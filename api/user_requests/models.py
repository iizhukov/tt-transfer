from django.db import models
from django.utils.translation import gettext_lazy as _

from api.address.models import Address
from api.profile.models import Client


class UserRequest(models.Model):
    from_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('Из'),
        related_name="from+",
    )
    to_address = models.ForeignKey(
        Address, models.CASCADE, verbose_name=_('В'),
        related_name="to"
    )
    client = models.ForeignKey(
        Client, models.CASCADE, verbose_name=_('Клиент')
    )
