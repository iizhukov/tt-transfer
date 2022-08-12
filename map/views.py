from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from api.address.models import CityZone, City


@xframe_options_exempt
@permission_classes((AllowAny, ))
def zones(request):
    region_ = request.GET.get("region")
    city_ = request.GET.get("city")

    city, created = City.objects.get_or_create(
        region=region_,
        city=city_
    )

    if created:
        city.save()

    return render(
        request,
        "zones.html",
        context={
            "city": city
        }
    )


@xframe_options_exempt
@permission_classes((AllowAny, ))
def route(request):
    context = {
        "lat1": request.GET.get("lat1"),
        "lon1": request.GET.get("lon1"),
        "lat2": request.GET.get("lat2"),
        "lon2": request.GET.get("lon2"),
    }

    region_ = request.GET.get("region")
    city_ = request.GET.get("city")

    if region_ and city_:
        city = City.objects.get_or_create(
            region=region_,
            city=city_
        )[0]

        context["city"] = city


    print(context)

    return render(
        request,
        "route.html",
        context=context
    )