from abc import ABC, abstractmethod


class BaseController(ABC):
    """
    This class represents the base controller interface to
    use in application models
    """

    @abstractmethod
    def store(self, data):
        """
        Store controller method
        :param data:
        :return:
        """
        pass

    @abstractmethod
    def get(self, data):
        """
        Show controller method
        :param data:
        :return:
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Index controller method
        :return:
        """
        pass

    @abstractmethod
    def get_by_id(self, id):
        """
        Index controller method
        :param: id
        :return:
        """
        pass

    @abstractmethod
    def update(self, data, id):
        """
        Update controller method
        :param data:
        :param id:
        :return:
        """
        pass

    @abstractmethod
    def destroy(self, id):
        """
        Destroy controller method
        :param id:
        :return:
        """
        pass

    @abstractmethod
    def destroy_all(self):
        """
        Destroy controller method
        :return:
        """
        pass

    @abstractmethod
    def get_all_distinct(self):
        """
        Destroy controller method
        :return:
        """
