
import datetime

from models.base_model import BaseModel
from peewee import *


class BaseStation(BaseModel):
    """
    This class is the base station model for storage data in database
    """
    status: str = CharField()
    city: str = CharField()
    fistal_num: str = CharField()
    service_num: str = CharField()
    num_ato_de_rf: str = CharField()
    num_station: str = CharField()
    address: str = CharField()
    uf: str = CharField()
    municipal: str = CharField()
    issue: str = CharField()
    technology: str = CharField()
    half_access: str = CharField()
    start_frequency: float = FloatField()
    end_frequency: float = FloatField()
    azimuth: str = CharField()
    station_type: str = CharField()
    infra_physical_classification: str = CharField()
    sharing_infra_physical: str = CharField()
    infra_sharing_avail: str = CharField()
    antenna_type: str = CharField()
    homologacao_antenna: str = CharField()
    antenna_gain: float = FloatField()
    gain_front_coast: str = CharField()
    angle_half_power: str = CharField()
    elevation: str = CharField()
    polarization: str = CharField()
    height: float = FloatField()
    homologacao_transmission: str = CharField()
    power_transmission: float = FloatField()
    latitude: float = FloatField()
    longitude: float = FloatField()
    latitude_dms: str = CharField()
    longitude_dms: str = CharField()
    code_debit_tfi: str = CharField()
    date_first_licensing: str = CharField()
    color: str = CharField(default='blue')
    icon: str = CharField(default='tower')
    is_to_move: bool = BooleanField(default=False)

    created_at: datetime = DateTimeField(default=datetime.datetime.now)


