from django.contrib import admin

from .models import (
    PriceToCarClass, IntracityTariff,
    ServiceToPrice, AdditionalHubZoneToPrice,
    HubToPrice, Tariff, IntercityTariff
)


admin.site.register(PriceToCarClass)
admin.site.register(IntracityTariff)
admin.site.register(AdditionalHubZoneToPrice)
admin.site.register(HubToPrice)
admin.site.register(Tariff)
admin.site.register(IntercityTariff)
admin.site.register(ServiceToPrice)
