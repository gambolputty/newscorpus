from pathlib import Path
from typing import cast

from sqlite_utils import Database as SQLiteUtilsDatabase
from sqlite_utils.db import Table

DEFAULT_DATABASE_PATH = (
    Path(__file__).parent.parent.parent.resolve().joinpath("newscorpus.db")
)


class Database:
    """
    Database wrapper class
    """

    def __init__(self, path: Path | str | None = None):
        self._db = SQLiteUtilsDatabase(path or DEFAULT_DATABASE_PATH)

        # create table if not exists
        if not self.get_table("articles").exists():
            self.create_table_articles()

    def create_table_articles(self):
        self._db.create_table(
            "articles",
            {
                "title": str,
                "description": str,
                "text": str,
                "url": str,
                "published_at": float,
                "source": int,
            },
            not_null=("title", "text", "url", "published_at", "source"),
            if_not_exists=True,
        )

        # create index on url column if not exists
        self.get_table("articles").create_index(
            ["url"], unique=True, if_not_exists=True
        )

    def close(self):
        self._db.close()

    def get_table(self, table_name: str) -> Table:
        return cast(Table, self._db[table_name])

    def get_rows_count(self, table_name: str) -> int:
        table = self.get_table(table_name)
        return table.count if table.exists() else 0

    def insert_articles(self, articles: list[dict]):
        """
        Insert articles into database. Returns number of inserted rows.
        """
        rows_count_before = self.get_rows_count("articles")
        self.get_table("articles").insert_all(
            articles,
            batch_size=100000,  # type: ignore
            ignore=True,  # type: ignore
        )
        rows_inserted_count = self.get_rows_count("articles") - rows_count_before

        return rows_inserted_count
