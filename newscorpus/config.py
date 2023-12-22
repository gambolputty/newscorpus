from configparser import ConfigParser
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.resolve()

# read config files from config.cfg with ConfigParser
config = ConfigParser()
config.read(ROOT_PATH.joinpath("config.cfg"))

DEBUG = config.getboolean("DEFAULT", "debug", fallback=False)
MAX_WORKERS = config.getint("DEFAULT", "max_workers", fallback=1)
KEEP_DAYS = config.getint("DEFAULT", "keep_days", fallback=2)
MIN_TEXT_LENGTH = config.getint("DEFAULT", "min_text_length", fallback=350)
