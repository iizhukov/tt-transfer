from typing import List, Tuple
from urllib.parse import urlencode
from fuzzywuzzy import fuzz

from .route import Route, RouteStatuses, Point
from api.address.models import City, Hub, GlobalAddress, Coordinate, Address
from api.tariffs.models import Tariff, HubToPrice, HubsToPriceModel, AbstractLocationToPrice
from api.request import DistanceAndDuration, GetCoordsByAddress, DadataAddressComplete


class URLMapController:
    ROUTE_MAP_URL = "/map/route/?"

    @staticmethod
    def get_route_url(points: List[Point], center_coords: Point = None):
        lats, lons = URLMapController._coords_parse(points)
        
        if not center_coords:
            center_coords = points[0]
        
        url = URLMapController.ROUTE_MAP_URL + urlencode({
            "lat": lats,
            "lon": lons,
            "center": center_coords.get_tuple(),
        }, True)

        return url

    @staticmethod
    def _coords_parse(points):
        lats, lons = [], []
        
        for point in points:
            lats.append(point.lat)
            lons.append(point.lon)
        
        return lats, lons


class LocationSearchController:
    @staticmethod
    def search(search: str):
        search_lower = f'%{"%".join(search.lower().replace(",", " ").split())}%'
        response = []

        # hubs = list(Hub.objects.filter(title_lower__contains=search_lower).values_list("title", flat=True))
        # global_addresses = list(GlobalAddress.objects.filter(address_lower__contains=search_lower).values_list("address", flat=True))
        # addresses = list(Address.objects.filter(address_lower__contains=search_lower).values_list("address", flat=True))

        hubs: List[Hub] = list(Hub.objects.raw(
        """
            SELECT * FROM address_hub
            WHERE title_lower ILIKE %s
        """, (search_lower, ), 
        ))
        global_addresses: List[GlobalAddress] = list(GlobalAddress.objects.raw(
        """
            SELECT * FROM address_globaladdress
            WHERE address_lower ILIKE %s
        """, (search_lower, ),
        ))
        addresses: List[Address] = list(Address.objects.raw(
        """
            SELECT * FROM address
            WHERE address_lower ILIKE %s
        """, (search_lower, ),
        ))
        
        response = [
            *map(lambda x: x.title, hubs),
            *map(lambda x: x.address, global_addresses),
            *map(lambda x: x.address, addresses),
        ]
        
        # hubs: List[str] = Hub.objects.all().values_list('title', flat=True)
        # global_addresses: List[str] = GlobalAddress.objects.all().values_list('address', flat=True)
        # addresses: List[str] = Address.objects.all().values_list('address', flat=True)
        
        # print(addresses)
        
        # lower_search = search.lower()
        
        # for hub in hubs:
        #     coincidence = fuzz.ratio(hub.lower(), lower_search)
        #     response.append((coincidence, hub))
            
        # for global_address in global_addresses:
        #     coincidence = fuzz.ratio(global_address.lower(), lower_search)
        #     response.append((coincidence, global_address))
            
        # for address in addresses:
        #     coincidence = fuzz.ratio(address.lower(), lower_search)
        #     response.append((coincidence, address.lower()))
        
        # response.sort(reverse=True)
        
        return response
    
    @staticmethod
    def address_search(search: str, limit: int):
        return DadataAddressComplete.search(search, limit)
    
    @staticmethod
    def parse_point(point: str):
        hub = Hub.objects.filter(title=point).first()
        
        if hub:
            return hub
        
        global_address = GlobalAddress.objects.filter(address=point).first()
        
        if global_address:
            return global_address

        address = Address.objects.filter(address=point).first()
        
        if address:
            return address
        
        return DadataAddressComplete.get(point)


class CostCalculationController:
    @staticmethod
    def count_price(points: list, car_class: str):
        first = points[0]
        
        routes = []
        print(points)
        
        for second in points[1:]:
            if type(first) in (dict, Address) and type(second) not in (dict, Address):
                if type(first) is dict:
                    city = City.objects.get(
                        city=first.get("city"),
                        region=first.get("region")
                    )
                elif type(second) is Address:
                    city = second.city

                if type(second) is Hub:
                    routes.append(
                        CostCalculationController.intercity__hub__basic(
                            city,
                            second,
                            car_class
                        )
                    )
                elif type(second) is GlobalAddress:
                    routes.append(
                        CostCalculationController.intercity__global_address__basic(
                            city,
                            second,
                            car_class
                        )
                    )
        
        return routes[0]

    @staticmethod
    def intercity__hub__basic(city: City, hub: Hub, car_class: str):
        tariff: Tariff

        try:
            tariff = Tariff.objects.get(
                city=city,
                type="basic"
            )
            
            if not tariff.intercity_tariff.hubs.filter(
                hub=hub
            ):
                raise Tariff.DoesNotExist
            
            intercity: HubsToPriceModel = tariff.intercity_tariff.hubs.get(hub=hub)
            
            return Route(
                RouteStatuses.OK,
                CostCalculationController._intercity_response_data(intercity, car_class)
            )

        except Tariff.DoesNotExist:
            return Route(
                RouteStatuses.NoTariff
            )
            
    @staticmethod
    def intercity__global_address__basic(city: City, global_address: GlobalAddress, car_class: str):
        tariff: Tariff

        try:
            tariff = Tariff.objects.get(
                city=city,
                type="basic"
            )
            
            if not tariff.intercity_tariff.global_addresses.filter(
                global_address=global_address
            ):
                raise Tariff.DoesNotExist
            
            intercity: HubsToPriceModel = tariff.intercity_tariff.global_addresses.get(global_address=global_address)
            
            return Route(
                RouteStatuses.OK,
                CostCalculationController._intercity_response_data(intercity, car_class)
            )

        except Tariff.DoesNotExist:
            return Route(
                RouteStatuses.NoTariff
            )
    
    @staticmethod
    def intercity__city__basic(city_from: City, city_to: City, car_class: str):
        tariff: Tariff

        try:
            tariff = Tariff.objects.get(
                city=city_from,
                type="basic"
            )
            
            if not tariff.intercity_tariff.cities.filter(
                city=city_to
            ):
                raise Tariff.DoesNotExist
            
            intercity: HubsToPriceModel = tariff.intercity_tariff.cities.get(city=city_to)
            
            return Route(
                RouteStatuses.OK,
                CostCalculationController._intercity_response_data(intercity, car_class)
            )

        except Tariff.DoesNotExist:
            return Route(
                RouteStatuses.NoTariff,
            )

    @staticmethod
    def _intercity_response_data(intercity: AbstractLocationToPrice, car_class: str):
        return {
            "distance": intercity.distance,
            "hours_duration": intercity.hours_duration,
            "minutes_duration": intercity.minutes_duration,
            "customer_price": intercity.prices.get(car_class=car_class).customer_price,
            "driver_price": intercity.prices.get(car_class=car_class).driver_price,
        }
    
    
    @staticmethod
    def intracity__hub__basic(city: City, hub: Hub, coordinates: Coordinate, car_class: str):
        tariff: Tariff
        
        try:
            tariff = Tariff.objects.get(
                city=city,
                type="basic"
            )
            
            if not tariff.intracity_tariff.hub_to_prices.filter(
                hub=hub
            ):
                raise Tariff.DoesNotExist
            
            intracity: HubToPrice = tariff.intracity_tariff.hub_to_prices.get(hub=hub)
            zone = intracity.get_zone_by_coords(coordinates)
            
            if zone:
                distance, hours, minutes = DistanceAndDuration.get(
                    hub.coordinate.get_string(), coordinates.get_string()
                )
                
                customer_price = intracity.prices.get(car_class=car_class).customer_price \
                    + zone.prices.get(car_class=car_class).customer_price

                driver_price = intracity.prices.get(car_class=car_class).driver_price \
                    + zone.prices.get(car_class=car_class).driver_price
                
                # url = URLMapController.get_route_url([
                #     Point.coordinate_to_point(hub.coordinate), Point.coordinate_to_point(coordinates)
                # ])
                
                return Route(
                    RouteStatuses.OK,
                    {
                        "distance": distance,
                        "hours_duration": hours,
                        "minutes_duration": minutes,
                        "customer_price": customer_price,
                        "driver_price": driver_price,
                        # "url": url
                    }
                )
            
            return Route(
                RouteStatuses.NoZone,
            )
        except Tariff.DoesNotExist:
            return Route(
                RouteStatuses.NoTariff
            )
            
    @staticmethod
    def intracity__coords__basic(city: City, coords1: Coordinate, coords2: Coordinate, car_class: str):
        tariff: Tariff
        
        try:
            tariff = Tariff.objects.get(
                city=city,
                type="basic"
            )
            
            if city.coords_in_zone(coords1) and city.coords_in_zone(coords2):
                prices = tariff.intracity_tariff.prices
            
                distance, hours, minutes = DistanceAndDuration.get(
                    coords1.get_string(), coords2.get_string()
                )

                customer_price = prices.get(car_class=car_class).customer_price
                driver_price = prices.get(car_class=car_class).driver_price
                
                # point1, point2 = Point.coordinate_to_point(coords1), Point.coordinate_to_point(coords2)
                # url = URLMapController.get_route_url([point1, point2])
                
                return Route(
                    RouteStatuses.OK,
                    {
                        "distance": distance,
                        "hours_duration": hours,
                        "minutes_duration": minutes,
                        "customer_price": customer_price,
                        "driver_price": driver_price,
                        # "url": url
                    }
                )

            return Route(
                RouteStatuses.NoCityZone,
            )
        except Tariff.DoesNotExist:
            return Route(
                RouteStatuses.NoTariff
            )
