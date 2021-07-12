
import datetime

from models.base_model import BaseModel
from peewee import *


class Log(BaseModel):
    """
    This class is the log model for storage data in database
    """
    type = CharField()
    message = TextField()
    stack_trace = TextField()

    created_at = DateTimeField(default=datetime.datetime.now)
