from requests import request
# from django.conf import settings

# from .models import Address

URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&units=imperial&key={}"
API = "AIzaSyAfJi4UNg3Oq95pBMrZC34ENnBdnSErrCU"
PAYLOAD = {}
HEADERS = {}

def get_distance_between_addresses(address1, address2):
    raw_address1 = address1.model_as_raw()
    raw_address2 = address2.model_as_raw()

    response = request(
        "GET",
        URL.format(raw_address1, raw_address2, API),
        headers=HEADERS,
        data=PAYLOAD
    )

    print(response.text)


def get_coords_of_city_center(region, city):
    raw_data = f"Россия, {region}, {city}"

    response = request(
        "GET",
        URL
    )
