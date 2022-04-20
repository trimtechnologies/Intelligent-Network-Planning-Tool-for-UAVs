
import datetime

from models.base_model import BaseModel
from peewee import *


class BaseStation(BaseModel):
    """
    This class is the base station model for storage data in database
    """
    status: str = CharField()
    entity: str = CharField()
    fistel_number: str = CharField()
    service_number: str = CharField()
    radio_frequency_authorization_number: str = CharField()
    station_number: str = CharField()
    address: str = CharField()
    address_complement: str = CharField()
    uf: str = CharField()
    county: str = CharField()
    registration: str = CharField()
    technology: str = CharField()
    access_resource: str = CharField()
    initial_frequency: float = FloatField()
    final_frequency: float = FloatField()
    azimute: str = CharField()
    station_type: str = CharField()
    physical_infrastructure_classification: str = CharField()
    physical_infrastructure_sharing: str = CharField()
    availability_sharing_physical_infrastructure: str = CharField()
    antenna_type: str = CharField()
    antenna_approval: str = CharField()
    antenna_gain: float = FloatField()
    gain_front_coast: str = CharField()
    half_power_angle: str = CharField()
    elevation_degree: str = CharField()
    polarization: str = CharField()
    height: float = FloatField()
    transmission_approval: str = CharField()
    transmit_power: float = FloatField()
    latitude: float = FloatField()
    longitude: float = FloatField()
    latitude_dms: str = CharField()
    longitude_dms: str = CharField()
    debit_code_tfi: str = CharField()
    date_of_licensing: str = CharField()
    date_of_first_licensing: str = CharField()
    network_number: str = CharField()
    item_id: str = CharField()
    date_validation: str = CharField()
    fistel_number_assoc: str = CharField()
    color: str = CharField(default='blue')
    icon: str = CharField(default='tower')
    is_to_move: bool = BooleanField(default=False)

    created_at: datetime = DateTimeField(default=datetime.datetime.now)


