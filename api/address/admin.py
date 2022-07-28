from django.contrib import admin

from .models import (
    Address, City, CityZone,
    Coordinate, PriceToCarClass
)


admin.site.register(Address)
admin.site.register(City)
admin.site.register(CityZone)
admin.site.register(Coordinate)
admin.site.register(PriceToCarClass)
