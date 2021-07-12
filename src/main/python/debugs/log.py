import logging

from src.main.python.exceptions.application_exception import ApplicationException
from src.main.python.support.logs import to_log_error, to_log_debug, to_log_fatal, to_log_warning, to_log_info
from src.main.python.support.path import get_project_root

# root = get_project_root()

# logger = logging.getLogger('application_log')
# hdlr = logging.FileHandler(str(root) + '/logs/ftplog.log')
# formatter = logging.Formatter('%(asctime)s \t %(levelname)s \t %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.INFO)

# logger.info('File successfully uploaded to ')

# to_log_error('vaca')
# to_log_debug('vaca')
# to_log_fatal('vaca')
# to_log_warning('vaca')
# to_log_info('vaca')

try:
    c = 1/0
except BaseException:
    to_log_error(ApplicationException().get_message())