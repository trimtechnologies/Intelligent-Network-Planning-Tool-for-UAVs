# Testing simlation of generating random points
from __future__ import division

import random

import numpy as np
import matplotlib.pyplot as plt
from haversine import haversine, Unit
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from math import pi, cos, sin, asin, atan2, sqrt

def convert_to_radians(degrees):
    return (degrees * pi) / 180


def convert_to_degree(radians):
    return (radians * 180) / pi


def randomCircumferencePoint(latitude, longitude, radius):
    radius = sqrt(random.random()) * radius

    sinLat = sin(convert_to_radians(latitude))
    cosLat = cos(convert_to_radians(latitude))

    EARTH_RADIUS = 6371000  # meters
    TWO_PI = pi * 2
    THREE_PI = pi * 3

    # Random bearing (direction out 360 degrees)
    bearing = random.random() * TWO_PI
    sinBearing = sin(bearing)
    cosBearing = cos(bearing)

    # Theta is the approximated angular distance
    theta = radius / EARTH_RADIUS
    sinTheta = sin(theta)
    cosTheta = cos(theta)

    rLatitude = asin(sinLat * cosTheta + cosLat * sinTheta * cosBearing)

    rLongitude = convert_to_radians(longitude) + atan2(
        sinBearing * sinTheta * cosLat,
        cosTheta - sinLat * sin(rLatitude)
    )

    # Normalize longitude L such that -PI < L < +PI
    rLongitude = ((rLongitude + THREE_PI) % TWO_PI) - pi

    return convert_to_degree(rLatitude), convert_to_degree(rLongitude)


def create_random_point(x0, y0, distance):
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


fig = plt.figure()
ax = host_subplot(111, axes_class=AA.Axes)

# ax.set_ylim(76,78)
# ax.set_xlim(13,13.1)
ax.set_autoscale_on(True)

latitude1, longitude1 = -21.244459, -44.995551
ax.plot(latitude1, longitude1, 'ro')

for i in range(1, 700):
    x, y = randomCircumferencePoint(latitude1, longitude1, 5)
    ax.plot(x, y, 'bo')
    dist = haversine((x, y), (latitude1, longitude1), Unit.METERS)
    print("Distance between points " + str(tuple([x, y])) + " is " + str(
        dist))  # a value approxiamtely less than 500 meters

plt.show()