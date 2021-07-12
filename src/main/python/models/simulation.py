
import datetime

from models.base_model import BaseModel
from peewee import *


class Simulation(BaseModel):
    """
    This class is the simulation model for storage data in database
    """
    propagation_model: str = CharField()
    number_of_solutions: str = CharField()
    distance_of_solutions: str = CharField()
    solutions: str = TextField()
    started_at: datetime = CharField()
    ended_at: datetime = CharField()
    execution_seconds: str = CharField()

    initial_latitude: str = CharField()
    initial_longitude: str = CharField()
    initial_height: str = CharField()
    initial_power_transmission: str = CharField()
    initial_objective_function: str = CharField()

    best_latitude: str = CharField()
    best_longitude: str = CharField()
    best_height: str = CharField()
    best_power_transmission: str = CharField()
    best_objective_function: str = CharField()

    created_at: datetime = DateTimeField(default=datetime.datetime.now)


