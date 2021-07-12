
from datetime import datetime

from controllers.base_controller import BaseController
from exceptions.application_exception import ApplicationException
from models.base_station import BaseStation
from support.logs import to_log_error


class BaseStationController(BaseController):
    """
    This class implement the base station controller
    """

    def __init__(self):
        """
        BaseStation controller constructor using service and repository
        """
        pass

    def store(self, data):
        """
        This method store a base station using the service
        :param data:
        :return:
        """
        try:
            return BaseStation.create(**data)

        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get(self, data):
        """
        This method show details for a specific base station
        :param data:
        :return:
        """
        pass

    def get_by_id(self, id) -> BaseStation:
        """
        This method show details for a specific base station
        :param id:
        :return:
        """

        try:
            return BaseStation.get(BaseStation.id == id)
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get_all(self):
        """
        This method get all details for base stations
        :return:
        """
        try:
            return BaseStation.select()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def update(self, data, id: int):
        """
        This method update a base station using a service
        :param data:
        :param id:
        :return:
        """

        base_station = BaseStation.get_by_id(id)

        try:
            data['updated_at'] = datetime.now()
            return base_station.update(data).where(BaseStation.id == id).execute()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def destroy(self, id: int):
        """
        This method delete a base station using a service
        :param id:
        :return:
        """
        try:
            model = BaseStation.get_by_id(id)

            return BaseStation.delete_by_id(model.id)
        except Exception as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def destroy_all(self):
        """
        This method delete all base station using a service
        :return:
        """
        try:
            return BaseStation.truncate_table()
        except Exception as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
            return None

    def get_all_distinct(self):
        """
        This method get all details for base stations
        :return:
        """
        try:
            return BaseStation.select().group_by(BaseStation.endereco).order_by(BaseStation.id).execute()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
