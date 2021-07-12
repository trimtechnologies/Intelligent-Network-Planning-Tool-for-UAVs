import re

from src.main.python.support.database import BaseStationDAO

base_station = {
    "status": "LIC-LIC-01",
    "entity": "TELEFÔNICA BRASIL S.A.",
    "num_fistel": 50409146285,
    "num_service": 10,
    "num_ato": 16972008,
    "num_station": 5101891,
    "address": "RUA DESEMBARGADOR SABINO LUSTOSA,S/N,CENTRO",
    "uf": "MG",
    "cod_country": 3138203,
    "emission": "5M00G9W",
    "initial_frequency": 2155.00000000,
    "final_frequency": 2165.00000000,
    "azimute": 300.0,
    "cod_station_type": "FB",
    "cod_antenna_type": 760,
    "cod_equipment_antenna": "27820904280",
    "gain_antenna": 16.0,
    "gain_coast_front_antenna": 32.0,
    "lifting_angle_antenna": 9.60,
    "half_power_angle": 71.00,
    "polarization": "X",
    "height": 70.0,
    "cod_equipment_transmitter": "18930701882",
    "transmission_power": "40000",
    "latitude": "21S151580",
    "longitude": "45W001490",
    "first_license_date": "17/08/1999",
}

base_station_dao = BaseStationDAO()


# base_station_dao.insert(base_station)
# base_station['status'] = 'vaca'
# base_station['created_at'] = '2019-08-19 12:41:49.480285'
# base_station_dao.update(3, base_station)
# base_station_dao.delete(1)
# for bs in base_station_dao.get_all():
#     print(bs)


def dms_to_dd(coordinate_in_dms):
    sign = -1 if re.search("[swSW]", coordinate_in_dms) else 1
    c = split_coordinates_dms(coordinate_in_dms)
    return sign * (float(c["d"]) + float(c["m"]) / 60 + float(c["s"]) / 3600)


def split_coordinates_dms(coordinate_in_dms):
    degrees = coordinate_in_dms[:2]
    minutes = coordinate_in_dms[3:5]
    seconds = coordinate_in_dms[5:7]
    seconds += "." + coordinate_in_dms[7:]

    return {"d": degrees, "m": minutes, "s": seconds}
