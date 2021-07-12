from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


# point = Feature(geometry=Point((-21.238864, -44.984765))) # false
# point = Feature(geometry=Point([-21.241922, -44.993992]))
# polygon = Polygon(
#     [
#         [
#             (-21.252142, -45.013754),
#             (-21.252142, -44.984765),
#             (-21.238862, -45.013754),
#             (-21.238862, -44.984765),
#         ]
#     ]
# )
# print(boolean_point_in_polygon(point, polygon))

def FindPoint(x1, y1, x2, y2, x, y):
    if (x > x1 and x < x2 and y > y1 and y < y2):
        return True
    else:
        return False


point = (-21.238864, -44.984765)
# point = [-21.241922, -44.993992]

print(FindPoint(-21.252142, -45.013754, -21.238862, -44.984765, point[0], point[1]))
