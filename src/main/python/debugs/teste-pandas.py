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
        "entidade": row[1],
        "num_fistel": row[2],
        "num_servico": row[3],
        "num_ato_de_rf": row[4],
        "num_estacao": row[5],
        "endereco": row[6],
        "uf": row[7],
        "municipio": row[8],
        "emissao": row[9],
        "tecnologia": row[10],
        "frequencia_inicial": row[11],
        "frequencia_final": row[12],
        "azimute": row[13],
        "tipo_estacao": row[14],
        "classificacao_infra_fisica": row[15],
        "compartilhamento_infra_fisica": row[16],
        "disp_compartilhamento_infra": row[17],
        "tipo_antena": row[18],
        "homologacao_antena": row[19],
        "ganho_antena": row[20],
        "ganho_frente_costa": row[21],
        "angulo_meia_potencia": row[22],
        "elevacao": row[23],
        "polarizacao": row[24],
        "altura": row[25],
        "homologacao_transmissao": row[26],
        "potencia_transmissao": row[27],
        "latitude": row[28],
        "longitude": row[29],
        "data_primeiro_licenciamento": row[30],
    }

    base_station_dao.insert(data)
    print(round(((i / total) * 100), 2), "%")
    i += 1
    # break
