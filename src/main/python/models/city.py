
import datetime

from models.base_model import BaseModel
from peewee import *

from models.state import State


class City(BaseModel):
    """
    This class is the state model for storage data in database
    """
    name = CharField()
    city_cod = IntegerField()

    state = ForeignKeyField(State, backref='cities', lazy_load=False)

    created_at = DateTimeField(default=datetime.datetime.now)
