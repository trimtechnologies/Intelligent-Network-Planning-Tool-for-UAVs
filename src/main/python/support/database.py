from peewee import SqliteDatabase

from support.settings import DATABASE_NAME
from support.path import get_project_root


def get_database_url() -> str:
    """
    This method return the path of database according to database name
    in .env file
    :return:
    """
    return str(get_project_root()) + '/database/' + str(DATABASE_NAME)


def get_sqlite_database_instance() -> SqliteDatabase:
    """
    This method return the sql database instance
    :return:
    """
    return SqliteDatabase(get_database_url())


def create_tables() -> None:
    """
    In this method creates all the tables in the database
    according to the application models
    :return:
    """

    # Import models locally
    from models.base_station import BaseStation
    from models.city import City
    from models.log import Log
    from models.simulation import Simulation
    from models.settings import Settings
    from models.state import State

    database = get_sqlite_database_instance()
    with database:
        database.create_tables([
            BaseStation, City, Log, Simulation, Settings, State
        ])
