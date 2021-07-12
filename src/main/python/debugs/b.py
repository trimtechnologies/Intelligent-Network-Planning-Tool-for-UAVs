from math import sin, cos, sqrt, atan2, radians
from haversine import haversine, Unit


# approximate radius of earth in km
R = 6373.0


lat1 = radians(-21.227136)
lon1 = radians(-44.978076)

lat2 = radians(-21.227136)
lon2 = radians(-44.977987)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance*1000, "m")

####################################
lyon = (-21.227136, -44.978076) # (lat, lon)
paris = (-21.227136, -44.977987)

print(haversine(lyon, paris, unit=Unit.METERS))
