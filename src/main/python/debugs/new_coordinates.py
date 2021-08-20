import random

from srtm import Srtm1HeightMapCollection
from srtm.base_coordinates import RasterBaseCoordinates
from haversine import haversine, Unit
from math import pi, cos, sin, sqrt, asin, atan2
import numpy as np


def convert_to_radians(degrees):
    return (degrees * pi) / 180


def convert_to_degree(radians):
    return (radians * 180) / pi


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


new_coordinates = get_coordinate_in_circle(-21.22611, -44.97806, 400)

# -21.223897093073102, -44.977260560886194
# -21.229288847346453, -44.97834468515236
# -21.224612017247477, -44.97722777455952
# -21.228540944480034, -44.9764680177349
print(new_coordinates)