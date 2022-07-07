# Load the Pandas libraries with alias 'pd'
import pandas as pd

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
from src.main.python.support.database import BaseStationDAO

data = pd.read_csv("csv_licenciamento_ecb6f784.csv", encoding="ISO-8859-1")
# Preview the first 5 lines of the loaded data

rows = data.get_values()

i = 0
total = len(rows)

base_station_dao = BaseStationDAO()
base_station_dao.delete_all()

for row in rows:
    data = {
        "status": row[0],
        "entity": row[1],
        "fistel_number": row[2],
        "service_number": row[3],
        "radio_frequency_authorization_number": row[4],
        "station_number": row[5],
        "address": row[6],
        "uf": row[7],
        "county": row[8],
        "registration": row[9],
        "technology": row[10],
        "initial_frequency": row[11],
        "final_frequency": row[12],
        "azimute": row[13],
        "station_type": row[14],
        "physical_infrastructure_classification": row[15],
        "physical_infrastructure_sharing": row[16],
        "antenna_type": row[17],
        "antenna_approval": row[18],
        "antenna_gain": row[19],
        "gain_front_coast": row[20],
        "half_power_angle": row[21],
        "elevation_degree": row[22],
        "polarization": row[23],
        "height": row[24],
        "transmission_approval": row[25],
        "transmit_power": row[26],
        "latitude": row[27],
        "longitude": row[28],
        "date_of_first_licensing": row[29],
    }

    base_station_dao.insert(data)
    print(round(((i / total) * 100), 2), "%")
    i += 1
    # break
