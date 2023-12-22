import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

LOG_DIR_PATH = Path(__file__).parent.parent.resolve().joinpath("logs")


def create_rotating_log(debug: bool = False):
    LOG_DIR_PATH.mkdir(exist_ok=True)

    logger = logging.getLogger("rotating_log")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    rotation_handler = RotatingFileHandler(
        LOG_DIR_PATH.joinpath("scraper_log"),
        maxBytes=1000000,
        backupCount=4,
        encoding="utf-8",
    )
    rotation_handler.setFormatter(
        logging.Formatter("%(levelname)s:%(asctime)s: %(message)s")
    )
    logger.addHandler(rotation_handler)

    # add stream handler for colored output
    stream_handler = colorlog.StreamHandler()
    stream_handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s: %(message)s"
        )  # noqa: E501
    )
    logger.addHandler(stream_handler)

    return logger
