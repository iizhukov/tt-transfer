import requests


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
        ).json()

        if response:
            print(response[0]["lat"], response[0]["lon"])

            return response[0]["lat"], response[0]["lon"]
        
        return None, None
