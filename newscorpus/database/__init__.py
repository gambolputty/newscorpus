import datetime
from pathlib import Path
from typing import cast

from pydantic import BaseModel, field_serializer
from sqlite_utils import Database as SQLiteUtilsDatabase
from sqlite_utils.db import Table

DEFAULT_DATABASE_PATH = (
    Path(__file__).parent.parent.parent.resolve().joinpath("newscorpus.db")
)


class Article(BaseModel):
    title: str
    description: str | None = None
    text: str
    url: str
    published_at: datetime.datetime
    source: int

    @field_serializer("published_at")
    def serialize_published_at(self, published_at: datetime.datetime, _info):
        return published_at.timestamp()


class Database:
    """
    Database wrapper class
    """

    def __init__(self, path: Path | str | None = None):
        self._db = SQLiteUtilsDatabase(path or DEFAULT_DATABASE_PATH)

        self.create_table_articles()
        self.create_indices()

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

    def create_indices(self):
        articles_table = self.get_table("articles")
        articles_table.create_index(["url"], unique=True, if_not_exists=True)
        articles_table.create_index(["published_at"], if_not_exists=True)

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

    @staticmethod
    def _import_articles_from_json(json_file_path: Path):
        """
        Import articles from old MongoDB json file
        """
        import json

        from dateparser import parse

        db = Database()
        db._db.execute("PRAGMA synchronous = OFF")

        # Begin a transaction
        db._db.execute("BEGIN")

        with open(json_file_path, "r") as f:
            try:
                for line in f:
                    old_article = json.loads(line)
                    published_at = parse(old_article["published_at"]["$date"])

                    if not published_at:
                        print("Could not parse date")
                        continue

                    new_article = Article(
                        title=old_article["title"],
                        description=None,
                        text=old_article["text"],
                        url=old_article["url"],
                        published_at=published_at,
                        source=old_article["src"],
                    )

                    news_article_dumped = new_article.model_dump()

                    # convert values to tuple
                    values = tuple(news_article_dumped.values())

                    db._db.execute(
                        "INSERT INTO articles (title, description, text, url, published_at, source) VALUES (?, ?, ?, ?, ?, ?)",
                        values,
                    )

                    # Commit the transaction
                    db._db.conn.commit()  # type: ignore

            except Exception as e:
                # Rollback the transaction if an error occurs
                db._db.conn.rollback()  # type: ignore
                print("Error:", str(e))
            finally:
                db.create_indices()
                db.close()
