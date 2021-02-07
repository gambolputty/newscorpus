import os
from pathlib import Path

env = os.getenv('PYTHON_ENV', 'development')

root = Path.cwd()
root = root.joinpath('app')

sources_path = root.joinpath('assets', 'sources.json')
assets_dir_path = root.joinpath('assets')
logs_dir_path = root.joinpath('logs')

# MongoDB
mongo_host = 'mongo'
mongo_port = 27017
mongo_username = os.getenv('MONGO_USER', 'admin')
mongo_password = os.getenv('MONGO_PASSWORD', '')
mongo_dbname = os.getenv("MONGO_DB_NAME", '')
create_mongo_text_index = os.getenv("MONGO_CREATE_TEXT_INDEX", 'False').lower() in ['true', '1']
