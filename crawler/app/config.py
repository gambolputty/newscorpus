import os
from pathlib import Path

ENV = os.getenv('PYTHON_ENV', 'development')

# paths
ROOT_PATH = Path.cwd()
ROOT_PATH = ROOT_PATH.joinpath('app')

SOURCES_PATH = ROOT_PATH.joinpath('assets', 'sources.json')
LOGS_PATH = ROOT_PATH.joinpath('logs')

# general
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '0')) or None
KEEP_DAYS = int(os.getenv('KEEP_DAYS', '2'))

# MongoDB
MONGO_HOST = 'mongo'
MONGO_PORT = 27017
MONGO_USERNAME = os.getenv('MONGO_USER', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", '')
MONGO_CREATE_TEXT_INDEX = os.getenv("MONGO_CREATE_TEXT_INDEX", 'False').lower() in ['true', '1']
