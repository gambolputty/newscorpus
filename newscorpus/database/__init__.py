from typing import cast

from sqlite_utils import Database as SQLiteUtilsDatabase
from sqlite_utils.db import Table

from newscorpus import config

DATABASE_PATH = config.ROOT_PATH.joinpath("newscorpus.db")


# A class to load the sqlite database and provide a connection to it.
class Database:
    def __init__(self):
        self._db = SQLiteUtilsDatabase(DATABASE_PATH)

    def get_db(self) -> SQLiteUtilsDatabase:
        return self._db

    def close(self):
        self._db.close()

    def get_table(self, table_name: str) -> Table:
        return cast(Table, self._db[table_name])
