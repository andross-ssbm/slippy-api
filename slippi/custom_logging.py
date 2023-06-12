import logging
import sys


format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'


def init():
    logger = logging.getLogger('slippy-api')
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler('log.log')

    stdout_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(format_string)
    stdout_handler.setFormatter(CustomFormatter())
    file_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = format_string

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def get_logger(self) -> logging.Logger:
        return logging.getLogger('slippy-api')

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatting = logging.Formatter(log_fmt)
        return formatting.format(record)

init()
