
from datetime import datetime

from controllers.base_controller import BaseController
from exceptions.application_exception import ApplicationException
from models.settings import Settings
from support.logs import to_log_error


class SettingsController(BaseController):
    """
    This class implement the setting controller
    """

    def __init__(self):
        """
        Settings controller constructor using service and repository
        """
        pass

    def store(self, data):
        """
        This method store a setting using the service
        :param data:
        :return:
        """
        try:
            return Settings.create(**data)

        except BaseException:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(e)
            return None

    def get(self, data):
        """
        This method show details for a specific setting
        :param data:
        :return:
        """
        print(data)

        try:
            return Settings.select().where(Settings.option == data['option']).get()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get_by_id(self, id):
        """
        This method show details for a specific setting
        :param id:
        :return:
        """

        try:
            return Settings.get(Settings.id == id)
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get_all(self):
        """
        This method show details for all settings
        :return:
        """
        try:
            return Settings.select().get()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def update(self, data, id):
        """
        This method update a setting using a service
        :param data:
        :param id:
        :return:
        """
        model = Settings.select().where(Settings.option == data['option']).get()

        settings = Settings.get_by_id(model.id)

        try:
            data['updated_at'] = datetime.now()
            return settings.update(data).where(Settings.id == model.id).execute()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def destroy(self, id):
        """
        This method delete a setting using a service
        :param id:
        :return:
        """
        try:
            model = Settings.get_by_id(id)

            return Settings.delete_by_id(model.id)
        except Exception as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def destroy_all(self):
        """
        This method delete all setting using a service
        :return:
        """
        try:
            return Settings.truncate_table()
        except Exception as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get_all_distinct(self):
        """
        This method get all details for settings
        :return:
        """
        try:
            return Settings.select().group_by(Settings.option).order_by(Settings.id).execute()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
