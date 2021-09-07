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
        "availability_sharing_physical_infrastructure": row[17],
        "antenna_type": row[18],
        "antenna_approval": row[19],
        "antenna_gain": row[20],
        "gain_front_coast": row[21],
        "half_power_angle": row[22],
        "elevation_degree": row[23],
        "polarization": row[24],
        "height": row[25],
        "transmission_approval": row[26],
        "transmit_power": row[27],
        "latitude": row[28],
        "longitude": row[29],
        "date_of_first_licensing": row[30],
    }

    base_station_dao.insert(data)
    print(round(((i / total) * 100), 2), "%")
    i += 1
    # break
