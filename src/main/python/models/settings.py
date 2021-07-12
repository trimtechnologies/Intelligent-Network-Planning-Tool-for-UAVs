
import datetime

from models.base_model import BaseModel
from peewee import *


class Settings(BaseModel):
    """
    This class is the settings model for storage data in database
    """
    option = CharField()
    value = CharField()

    updated_at = DateTimeField(default=datetime.datetime.now)
