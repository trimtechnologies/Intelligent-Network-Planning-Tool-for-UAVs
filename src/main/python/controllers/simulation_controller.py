
from datetime import datetime

from controllers.base_controller import BaseController
from exceptions.application_exception import ApplicationException
from models.simulation import Simulation
from support.logs import to_log_error


class SimulationController(BaseController):
    """
    This class implement the base station controller
    """

    def __init__(self):
        """
        Simulation controller constructor using service and repository
        """
        pass

    def store(self, data):
        """
        This method store a base station using the service
        :param data:
        :return:
        """
        try:
            return Simulation.create(**data)

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

    def get_by_id(self, id) -> Simulation:
        """
        This method show details for a specific base station
        :param id:
        :return:
        """

        try:
            return Simulation.get(Simulation.id == id)
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
            return Simulation.select()
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

        base_station = Simulation.get_by_id(id)

        try:
            data['updated_at'] = datetime.now()
            return base_station.update(data).where(Simulation.id == id).execute()
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
            model = Simulation.get_by_id(id)

            return Simulation.delete_by_id(model.id)
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
            return Simulation.truncate_table()
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
            return Simulation.select().group_by(Simulation.endereco).order_by(Simulation.id).execute()
        except BaseException as be:
            e = ApplicationException()
            to_log_error(e.get_message())
            print(be)
            print(e)
