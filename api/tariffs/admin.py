from django.contrib import admin

from .models import (
    PriceToCarClass, IntracityTariff,
    ZoneToPrice, ServiceToPrice
)


admin.site.register(PriceToCarClass)
admin.site.register(IntracityTariff)
admin.site.register(ZoneToPrice)
admin.site.register(ServiceToPrice)
