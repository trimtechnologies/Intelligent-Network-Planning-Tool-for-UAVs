from peewee import *

from support.database import get_database_url

database = SqliteDatabase(get_database_url())

"""
Link to peewee models documentation
http://docs.peewee-orm.com/en/latest/peewee/models.html
"""


class BaseModel(Model):
    """
    This class is the base model for all models of application
    """

    class Meta:
        """
        This method is used for Peewee model
        """
        database = database
