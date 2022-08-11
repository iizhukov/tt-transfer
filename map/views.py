from django.shortcuts import render

from api.address.models import CityZone, City

def index(request):
    region_ = request.GET.get("region")
    city_ = request.GET.get("city")

    city = City.objects.filter(
            region=region_,
            city=city_
    ).first()

    print(city)

    latitude = city.center.latitude
    longitude = city.center.longitude

    return render(
        request,
        "index.html",
        context={
            "region": region_,
            "city": city_,
            "city_latitude": latitude,
            "city_longitude": longitude,
        }
    )
