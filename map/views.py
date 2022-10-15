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

    city = City.objects.get(
        region=region_,
        city=city_
    )

    return render(
        request,
        "zones.html",
        context={
            "city": city,
            "lat": request.GET.getlist("lat"),
            "lon": request.GET.getlist("lon"),
            "title": request.GET.getlist("title")
        }
    )
    
    
@xframe_options_exempt
@permission_classes((AllowAny, ))
def route(request):
    center_lat, center_lon = request.GET.getlist("center")
    
    context = {
        "lat": request.GET.getlist("lat"),
        "lon": request.GET.getlist("lon"),
        "center_lat": center_lat,
        "center_lon": center_lon
    }

    return render(
        request,
        "route.html",
        context=context
    )


@xframe_options_exempt
@permission_classes((AllowAny, ))
def route_old(request):
    context = {
        "lat": request.GET.getlist("lat"),
        "lon": request.GET.getlist("lon"),
    }

    print(request.GET)

    region_ = request.GET.get("region")
    city_ = request.GET.get("city")

    if region_ and city_:
        city = City.objects.get(
            region=region_,
            city=city_
        )

        context["city"] = city

    print(context)

    return render(
        request,
        "route.html",
        context=context
    )