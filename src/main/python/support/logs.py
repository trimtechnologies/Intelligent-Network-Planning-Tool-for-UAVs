import logging

from models.log import Log
from support.path import get_project_root

root = get_project_root()

formatter = logging.Formatter('%(levelname)s - \t %(asctime)s -->\t  %(message)s')


def log_to_database(type: str, message: str, stack_trace: str) -> None:
    """
    This method save a exception log in database
    :param type: Type of log
    :param message: Message of log
    :param stack_trace: Stack of exception log
    :return: None
    """
    Log.create(type=type, message=message, stack_trace=stack_trace)


def to_log_error(log_text: str) -> None:
    """
    This method write the informed text log in error log file
    :param string log_text: The text to log
    :return: None
    """
    logger = logging.getLogger('application_error_log')
    file_handler = logging.FileHandler(str(root) + '/logs/error.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.ERROR)

    logger.error(log_text)


def to_log_debug(log_text: str) -> None:
    """
    This method write the informed text log in debug log file
    :param string log_text: The text to log
    :return: None
    """
    logger = logging.getLogger('application_debug_log')
    file_handler = logging.FileHandler(str(root) + '/logs/debug.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.debug(log_text)


def to_log_fatal(log_text: str) -> None:
    """
    This method write the informed text log in fatal log file
    :param string log_text: The text to log
    :return: None
    """
    logger = logging.getLogger('application_fatal_log')
    file_handler = logging.FileHandler(str(root) + '/logs/fatal.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.FATAL)

    logger.fatal(log_text)


def to_log_warning(log_text: str) -> None:
    """
    This method write the informed text log in warning log file
    :param string log_text: The text to log
    :return: None
    """
    logger = logging.getLogger('application_warning_log')
    file_handler = logging.FileHandler(str(root) + '/logs/warning.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.WARNING)

    logger.warning(log_text)


def to_log_info(log_text: str) -> None:
    """
    This method write the informed text log in info log file
    :param string log_text: The text to log
    :return: None
    """
    logger = logging.getLogger('application_info_log')
    file_handler = logging.FileHandler(str(root) + '/logs/info.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    logger.warning(log_text)
