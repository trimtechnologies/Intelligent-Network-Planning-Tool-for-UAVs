
import datetime

from models.base_model import BaseModel
from peewee import *


class State(BaseModel):
    """
    This class is the state model for storage data in database
    """
    cod_uf = IntegerField()
    sigla_uf = CharField()

    created_at = DateTimeField(default=datetime.datetime.now)
