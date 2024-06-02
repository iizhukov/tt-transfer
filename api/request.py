import requests
from dadata import Dadata
from pprint import pprint


class GetCoordsByAddress:
    URL = "https://nominatim.openstreetmap.org/search"
    payload = {
        "format": "json",
        "polygon": "1",
        "addressdetails": "1",
    }

    @staticmethod
    def get(address):
        GetCoordsByAddress.payload["q"] = address

        response = requests.get(
            GetCoordsByAddress.URL,
            params=GetCoordsByAddress.payload
        )
        
        print(response.raw)
        
        response = response.json()

        if response:
            print(response[0]["lat"], response[0]["lon"])

            return response[0]["lat"], response[0]["lon"]
        
        return None, None


class DistanceAndDuration:
    api_key = "25e84449-a26b-44b4-b580-f18cd9d2723e"
    URL = f"https://graphhopper.com/api/1/route"
    payload = {
        "point": [],
        "profile": "car",
        "locale": "ru",
        "calc_points": "false",
        "key": api_key
    }

    @staticmethod
    def get(city_coord1, city_coord2, additional_races=None, format=True):

        points = [city_coord1, city_coord2]
        if additional_races:
            points.insert(1, *additional_races)

        # print(points)
        
        print(points)

        DistanceAndDuration.payload["point"] = points

        try:
            response = requests.get(
                DistanceAndDuration.URL,
                params=DistanceAndDuration.payload
            ).json()

            paths = response["paths"][0]

            if format:
                distance = round(paths["distance"] / 1000, 2)
                hours = paths["time"] // 3.6e6
                minutes = (paths["time"] - hours * 3.6e6) // 6e4

                # print(distance, int(hours), int(minutes))

                return distance, int(hours), int(minutes)
            
            return paths["distance"], paths["time"]
        except KeyError as e:
            return None, None, None

    @staticmethod
    def __decode_coords(city_coord1, city_coord2, additional_races=None):
        if type(city_coord1) in (list, tuple, set):
            city_coord1 = ", ".join(list(map(str, city_coord1)))
        
        if type(city_coord2) in (list, tuple, set):
            city_coord2 = ", ".join(list(map(str, city_coord2)))

        if additional_races:
            additional_races = [
                ", ".join(list(map(str, race)))
                if race in (list, tuple, set) else race
                for race in additional_races
            ]
        
        return  city_coord1, city_coord2, additional_races


class DadataAddressComplete:
    TOKEN = "48ab36191d6ef5b11a3ae58d406b7d641a1fbd32"
    DADATA = Dadata(TOKEN)
    
    def search(search: str, limit=None):
        result = DadataAddressComplete.DADATA.suggest("address", search)
        
        if not result:
            return None
        
        response = [
            res.get("value")
            for res in result
        ]
        
        if limit:
            response = response[:limit]
        
        return response
    
    def get(address: str):
        result = DadataAddressComplete.DADATA.suggest("address", address)

        if not result:
            return None
        
        result = result[0]
        
        region = result.get("data", {}).get("region", "")
        region_type = result.get("data", {}).get("region_type_full", "")
        
        if region_type == "область":
            region = f"{region} {region_type}".capitalize()
        elif region_type == "республика":
            region = f"{region_type} {region}".title()
        elif region_type == "автономный округ":
            region = region.replace("Автономный округ", "АО")
            
        return {
            "address": result.get("value"),
            "city": result.get("data", {}).get("city"),
            "region": region,
            "lat": result.get("data", {}).get("geo_lat"),
            "lon": result.get("data", {}).get("geo_lon")
        }


if __name__ == "__main__":
    # DistanceAndDuration.get("55.755819, 37.617644", "51.768205, 55.096964")
    pprint(DadataAddressComplete.search("Оренбург Монтажников 23"))
