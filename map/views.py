from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from api.address.models import CityZone, City


@xframe_options_exempt
def zones(request):
    region_ = request.GET.get("region")
    city_ = request.GET.get("city")

    city = City.objects.filter(
            region=region_,
            city=city_
    ).first()

    print(city)

    return render(
        request,
        "zones.html",
        context={
            "city": city
        }
    )
