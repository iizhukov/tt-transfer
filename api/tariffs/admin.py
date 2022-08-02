from django.contrib import admin

from .models import (
    PriceToCarClass, IntracityTariff,
)


admin.site.register(PriceToCarClass)
admin.site.register(IntracityTariff)
