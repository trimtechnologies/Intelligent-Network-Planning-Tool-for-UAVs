import random

from srtm import Srtm1HeightMapCollection
from srtm.base_coordinates import RasterBaseCoordinates
from haversine import haversine, Unit
from math import pi, cos, sin, sqrt, asin, atan2
import numpy as np

from support.physical_constants import r_earth

srtm1_data = Srtm1HeightMapCollection()
srtm1_data.build_file_index()
srtm1_data.load_area(RasterBaseCoordinates.from_file_name("S22W045"), RasterBaseCoordinates.from_file_name("S22W046"))


def get_altitude(lat: float, long: float) -> int:
    # Erro médio entre 1m e 2m
    return srtm1_data.get_altitude(latitude=lat, longitude=long)


def calculates_distance_between_coordinates(point_1: tuple, point_2: tuple, unit=Unit.METERS) -> float:
    return haversine(point_1, point_2, unit=unit)


def get_new_lat_lng(latitude: float, longitude: float, dx: float = 3, dy: float = 3) -> tuple:
    new_latitude = latitude + (round(dy / r_earth, 6)) * (round(180 / pi, 6))
    new_longitude = longitude + (round(dx / r_earth, 6)) * (round(180 / pi, 6)) / cos(round(latitude * pi / 180, 6))
    return tuple(((new_latitude), (new_longitude)))


def convert_to_radians(degrees):
    return (degrees * pi) / 180


def convert_to_degree(radians):
    return (radians * 180) / pi


def create_random_point_v2(x0, y0, distance):
    """
    Utility method for simulation of the points
    """
    r = distance / 111300
    u = np.random.uniform(0, 1)
    v = np.random.uniform(0, 1)
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    x1 = x / np.cos(y0)
    y = w * np.sin(t)
    return x0 + x1, y0 + y


def get_coordinate_in_circle(latitude: float, longitude: float, radius: float) -> tuple:
    """
    Metodo responsável por retornar uma nova coordenada dentro de um raio
    :param latitude: Latitude do ponto de referência
    :param longitude: Longitude do ponto de referência
    :param radius: raio maximo dados em metros para sorteio do ponto
    :rtype: object
    """
    radius = sqrt(random.random()) * radius

    sin_lat = sin(convert_to_radians(latitude))
    cos_lat = cos(convert_to_radians(latitude))

    earth_radius = 6371000  # meters
    two_pi = pi * 2
    three_pi = pi * 3

    # Random bearing (direction out 360 degrees)
    bearing = random.random() * two_pi
    sin_bearing = sin(bearing)
    cos_bearing = cos(bearing)

    # Theta is the approximated angular distance
    theta = radius / earth_radius
    sin_theta = sin(theta)
    cos_theta = cos(theta)

    r_latitude = asin(sin_lat * cos_theta + cos_lat * sin_theta * cos_bearing)

    r_longitude = convert_to_radians(longitude) + atan2(sin_bearing * sin_theta * cos_lat,
                                                        cos_theta - sin_lat * sin(r_latitude))

    # Normalize longitude L such that -PI < L < +PI
    r_longitude = ((r_longitude + three_pi) % two_pi) - pi

    # ToDo: tratar os bounds aqui

    lat, long = convert_to_degree(r_latitude), convert_to_degree(r_longitude)

    return tuple([lat, long])
