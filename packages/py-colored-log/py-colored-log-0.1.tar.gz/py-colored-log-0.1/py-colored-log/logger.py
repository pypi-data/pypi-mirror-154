import logging
import datetime
import CustomFormatter


def init_logging(log_level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s'):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    today = datetime.date.today()

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(CustomFormatter(format))

    file_handler = logging.FileHandler('{}.log'.format(today.strftime('%Y_%m_%d')))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(format))

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger
