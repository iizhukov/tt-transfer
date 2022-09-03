import requests
import json

from .models import City


def get_cities():
    r = requests.get("https://api.hh.ru/areas")
    regions = r.json()[0]["areas"]

    for region in regions:
        for city in region["areas"]:
            region_ = region["name"]
            city_ = city["name"].split("(")[0].strip()

            yield (region_, city_)


def create_cities():
    for region, city in get_cities():
        print(
            City.objects.get_or_create(
                region=region,
                city=city
            )
        )


def clear_cities_with_out_center_coordinates(delete=False):
    cities = City.objects.filter(
        center=None
    )
    print(len(cities))

    if delete:
        cities.delete()
