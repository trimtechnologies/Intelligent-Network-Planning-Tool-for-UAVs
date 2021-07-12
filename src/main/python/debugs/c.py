import math
import random

lat = 19.99
lon = 73.78

dec_lat = random.random() / 100
dec_lon = random.random() / 100
print('%.6f %.6f \n' % (lon + dec_lon, lat + dec_lat))
