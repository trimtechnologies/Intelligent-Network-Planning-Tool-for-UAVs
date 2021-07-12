import pandas as pd
import requests
import re

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

from pandas import DataFrame

import support.constants as constants
from exceptions.application_exception import ApplicationException
from support.logs import to_log_error

# site: https://sistemas.anatel.gov.br/se/public/view/b/licenciamento.php

uf_list = {
    "RO": 11,
    "RR": 14,
    "AP": 16,
    "TO": 17,
    "PI": 22,
    "RN": 24,
    "PE": 26,
    "BA": 29,
    "RJ": 33,
    "SC": 42,
    "MT": 51,
    "AL": 27,
    "MG": 31,
    "PR": 41,
    "MS": 50,
    "DF": 53,
    "AC": 12,
    "AM": 13,
    "PA": 15,
    "MA": 21,
    "CE": 23,
    "PB": 25,
    "SE": 28,
    "ES": 32,
    "SP": 35,
    "RS": 43,
    "GO": 52,
}


def get_ufs_initials() -> list:
    """
    This method return the ufs initials ordered
    :return: list The of ufs ordered
    """
    return sorted(uf_list.keys())


def get_uf_code(uf: str) -> list:
    """
    This method return the uf code from ufs list
    :param uf: string The uf name
    :return: int Return the uf code
    """
    return uf_list.get(uf)


def get_uf_by_id(uf_id: int) -> str:
    """
    This method return the uf code from ufs list
    :param uf_id: int The uf id
    :return: string Return the uf initials
    """
    for uf, uf_code in uf_list.items():
        if uf_code == uf_id:
            return uf


def get_counties(uf: str) -> str:
    """
    This method get all counties from an uf related
    :param uf: int The uf code
    :return:
    """
    url_base = (
        "http://sistemas.anatel.gov.br/se/eApp/forms/b/jf_getMunicipios.php?CodUF="
    )
    uf_code = get_uf_code(uf)

    if uf_code:
        url = url_base + str(uf_code)
        try:
            return requests.get(url=url).json()
        except BaseException as be:
            print(be)
            e = ApplicationException()
            to_log_error(e.get_message())
            return constants.REQUEST_ERROR
    else:
        return constants.INVALID_UF


def dms_to_dd(coordinate_in_dms: str) -> float:
    # print(coordinate_in_dms)
    sign = -1 if re.search("[swSW]", coordinate_in_dms) else 1
    c = split_coordinates_dms(coordinate_in_dms)
    dd = sign * (float(c["d"]) + float(c["m"]) / 60 + float(c["s"]) / 3600)
    return round(dd, 6)


def split_coordinates_dms(coordinate_in_dms: str) -> dict:
    degrees = coordinate_in_dms[:2]
    minutes = coordinate_in_dms[3:5]
    seconds = coordinate_in_dms[5:7]
    seconds += "." + coordinate_in_dms[7:]

    return {"d": degrees, "m": minutes, "s": seconds}


def get_anatel_data(uf_sigle: str, country_id: int = None) -> DataFrame:
    """
    Get ERB info in Anatel online database
    :return: Pandas object
    """
    url_base = "http://sistemas.anatel.gov.br"
    request_url = url_base + "/se/public/view/b/export_licenciamento.php"

    parameters = {
        "qidx": 0,
        "skip": 0,  # quantidade de linhas a pular
        "filter": 1,  # se filtro aplicado ou nao
        "rpp": 50,  # quantidade por página
        "sort_0": 0,  # status
        "sort_1": 0,  # entidade
        "sort_2": 0,  # fistel
        "sort_3": 0,  # num servico
        "sort_4": 0,  # ato de rf
        "sort_5": 0,  # num estacao
        "sort_6": 0,  # endereco
        "sort_7": 0,  # UF
        "sort_8": 0,  # Municipio
        "sort_9": 0,  # emissao
        "sort_10": 0,  # tecnologia
        "sort_11": 0,  # meio acesso
        "sort_12": 0,  # freq ini
        "sort_13": 0,  # freq final
        "sort_14": 0,  # azimute
        "sort_15": 0,  # tipo estacao
        "sort_16": 0,  # classificacao infra fisica
        "sort_17": 0,  # compatilhamentro infa fisica
        "sort_18": 0,  # disp compartilhamento infra
        "sort_19": 0,  # tipo antena
        "sort_20": 0,  # homologacao antena
        "sort_21": 0,  # ganho antena
        "sort_22": 0,  # frente costa
        "sort_23": 0,  # angulo meia potencia
        "sort_24": 0,  # elevacao
        "sort_25": 0,  # polarizacao
        "sort_26": 0,  # altura antena
        "sort_27": 0,  # homologacao transmissao
        "sort_28": 0,  # potencia transmissao
        "sort_29": 0,  # latitude
        "sort_30": 0,  # longitude
        "sort_31": 0,  # cod deb tfi
        "sort_32": 0,  # data primeiro licenciamento
        "fc_0": None,  # status
        "fc_1": None,  # entidade
        "fc_2": None,  # fistel
        "fc_3": None,  # num servico
        "fc_4": None,  # ato de rf
        "fc_5": None,  # num estacao
        "fc_6": None,  # endereco
        "fc_7": uf_sigle,  # UF
        "fc_8": country_id,  # Municipio
        "fc_9": None,  # emissao
        "fc_10": None,  # tecnologia
        "fc_11": None,  # meio acesso
        "fc_12": None,  # freq ini
        "fc_13": None,  # freq final
        "fc_14": None,  # azimute
        "fc_15": None,  # tipo estacao
        "fc_16": None,  # classificacao infra fisica
        "fc_17": None,  # compatilhamentro infa fisica
        "fc_18": None,  # dissicao compartilhamento infra
        "fc_19": None,  # tipo antena
        "fc_20": None,  # homologacao antena
        "fc_21": None,  # ganho antena
        "fc_22": None,  # frente costa
        "fc_23": None,  # angulo meia potencia
        "fc_24": None,  # elevacao
        "fc_25": None,  # polarizacao
        "fc_26": None,  # altura antena
        "fc_27": None,  # homologacao transmissao
        "fc_28": None,  # potencia transmissao
        "fc_29": None,  # latitude
        "fc_30": None,  # longitude
        "fc_31": None,  # cod deb tfi
        "fc_32": None,  # data primeiro licenciamento
        "wfid": "licencas",
        "view": 0
    }

    print("Performing request with informed parameters ...")
    response = requests.post(
        request_url,
        data=parameters,
    ).json()

    if len(response) == 1:
        redirect_url = response["redirectUrl"]
        file_name = redirect_url.split("=")[1] + ".zip"

        try:
            print("Please wait, downloading the file '%s'..." % file_name)

            with urlopen(url_base + redirect_url) as f:
                with BytesIO(f.read()) as b, ZipFile(b) as zipfile:
                    file = zipfile.open(zipfile.namelist()[0])
                    df = pd.read_csv(file, encoding="ISO-8859-1")

            print("Download successful!")
            return df
        except requests.exceptions.RequestException as e:
            print(e)
            print("An error occurred while downloading ...")

    else:
        print(response["title"])
        print(response["message"])
