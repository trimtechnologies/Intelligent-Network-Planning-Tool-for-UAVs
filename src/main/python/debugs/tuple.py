FOs = []

FOs.append({
            "lat": "-41,123123",
            "lng": "-41,123123",
            "of": 60
        })
FOs.append({
            "lat": "-41,123123",
            "lng": "-41,123123",
            "of": 59
        })
FOs.append({
            "lat": "-41,123123",
            "lng": "-41,123123",
            "of": 12
        })
FOs.append({
            "lat": "-41,123123",
            "lng": "-41,123123",
            "of": 23
        })
FOs.append({
            "lat": "-41,123123",
            "lng": "-41,123123",
            "of": 45
        })

FOs_plot = [item['of'] for item in FOs]

print(FOs_plot)

from haversine import haversine, Unit

def calculates_distance_between_coordinates(point_1: tuple, point_2: tuple, unit=Unit.METERS) -> float:
    return haversine(point_1, point_2, unit=unit)

d = calculates_distance_between_coordinates(
                (-21.22811129472869,-44.981269684763), (-21.226219, -44.978219))

print(d)