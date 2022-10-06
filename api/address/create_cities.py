import requests
import json

from .models import City

FEDERAL_CITIES = ("Москва", "Санкт-Петербург", "Севастополь")
NEW_RU_CITIES_BY_REGION = ("Луганская область", "Донецкая область", "Херсонская область", "Запорожская область")


def get_cities():
    r = requests.get("https://api.hh.ru/areas")
    regions = r.json()[0]["areas"]

    for region in regions:
        for city in region["areas"]:
            region_ = region["name"]
            city_ = city["name"].split("(")[0].strip()

            yield (region_, city_)


def create_federal_cities():
    for city in FEDERAL_CITIES:
        print(
            City.objects.get_or_create(
                region=city,
                city=city
            )
        )


def create_cities():
    for region, city in get_cities():
        print(region, city)
        print(
            City.objects.get_or_create(
                region=region,
                city=city
            )
        )
    create_federal_cities()


def clear_cities_with_out_center_coordinates(delete=False):
    cities = City.objects.filter(
        center=None
    )
    print(len(cities))

    if delete:
        cities.delete()
