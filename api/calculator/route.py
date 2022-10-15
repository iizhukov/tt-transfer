from dataclasses import dataclass
from typing import Dict

from api.exceptions import RouteException


class RouteStatusObject:
    def __init__(self, status, detail) -> None:
        self.status = status
        self.detail = detail
    
    @property
    def is_success(self):
        return 200 <= self.status < 300


@dataclass
class RouteStatuses:
    OK = RouteStatusObject(200, "OK")
    NoTariff = RouteStatusObject(404, "Тариф не найден")
    NoZone = RouteStatusObject(401, 'Зона не найдена')
    
    NoCityZone = RouteStatusObject(401, "Одна или несколько точек не принадлежат городу")


class Route:
    def __init__(self, status: RouteStatusObject, data: Dict={}) -> None:
        self.status = status
        self.data = data
        
    def is_valid(self, raise_exception: bool=False):
        if not self.status.is_success:
            raise RouteException(self.status.detail)


class Point:
    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def get_tuple(self):
        return self.lat, self.lon
    
    def __str__(self) -> str:
        return f"{self.lat}, {self.lon}"
    
    def __repr__(self) -> str:
        return f"Point({self.lat}, {self.lon})"
    
    @staticmethod
    def coordinate_to_point(coordinate):
        return Point(
            lat=coordinate.latitude,
            lon=coordinate.longitude
        )
