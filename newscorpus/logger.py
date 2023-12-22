import logging
from logging.handlers import RotatingFileHandler

import colorlog

from newscorpus import config

# logger examples: https://www.programcreek.com/python/example/1475/logging.handlers.RotatingFileHandler # noqa: E501


def create_rotating_log():
    logs_dir_path = config.ROOT_PATH.joinpath("logs")
    logs_dir_path.mkdir(exist_ok=True)

    logger = logging.getLogger("rotating_log")
    logger.setLevel(logging.INFO if not config.DEBUG else logging.DEBUG)

    rotation_handler = RotatingFileHandler(
        logs_dir_path.joinpath("crawler_log"),
        maxBytes=1000000,
        backupCount=4,
        encoding="utf-8",
    )
    rotation_handler.setFormatter(
        logging.Formatter("%(levelname)s:%(asctime)s: %(message)s")
    )
    logger.addHandler(rotation_handler)

    # add stream handler in debug mode
    if config.DEBUG:
        stream_handler = colorlog.StreamHandler()
        stream_handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(levelname)s: %(message)s"
            )  # noqa: E501
        )
        logger.addHandler(stream_handler)

    return logger
