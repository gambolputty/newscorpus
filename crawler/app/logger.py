import os
import logging
from logging.handlers import RotatingFileHandler
import colorlog

from app import config

# logger examples: https://www.programcreek.com/python/example/1475/logging.handlers.RotatingFileHandler

# create log folder if not exist
if os.path.isdir(config.logs_dir_path) is False:
    os.mkdir(config.logs_dir_path)


def create_rotating_log(path):
    """
    Creates a rotating log
    """
    logger = logging.getLogger('rotating_log')
    logger.setLevel(logging.DEBUG if config.env == 'development' else logging.INFO)
    rotation_handler = RotatingFileHandler(path, maxBytes=1000000, backupCount=4, encoding='utf-8')
    rotation_handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s: %(message)s'))
    logger.addHandler(rotation_handler)

    # create console handler in dev mode
    stream_handler = colorlog.StreamHandler()
    stream_handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(asctime)s: %(message)s'))
    logger.addHandler(stream_handler)
