from math import pi, cos

r_earth = 6378
dy, dx = 1, 0

latitude, longitude = -21.243496, -45.004072

new_latitude = latitude + (round(dy / r_earth, 6)) * (round(180 / pi, 6))
new_longitude = longitude + (round(dx / r_earth, 6)) * (round(180 / pi, 6)) / cos(round(latitude * pi / 180, 6))
print(round(new_latitude, 6), round(new_longitude, 6))
