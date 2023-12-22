from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from sqlite_utils.db import Table

from newscorpus import config
from newscorpus.database import Database
from newscorpus.logger import create_rotating_log
from newscorpus.scraper import Article, scrape_source
from newscorpus.sources import SourceCollection


def insert_articles(articles: list[Article], db_table: Table):
    """Insert articles into database"""

    db_table.insert_all(
        [article.model_dump() for article in articles],
        batch_size=100000,  # type: ignore
        ignore=True,  # type: ignore
    )

    # create index on url column if not exists
    db_table.create_index(["url"], unique=True, if_not_exists=True)


def init():
    start_time = datetime.now()
    logger = create_rotating_log()
    logger.info("Downloading new articles")
    logger.info(f"Ignoring articles older than {config.KEEP_DAYS} days")
    db = Database()
    db_table = db.get_table("articles")

    if config.MAX_WORKERS:
        logger.info(f"Maximum crawler workers: {config.MAX_WORKERS}")

    sources = SourceCollection.from_file().root

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        for source, articles in executor.map(scrape_source, sources):
            rows_count_before = db_table.count
            insert_articles(articles, db_table)
            rows_inserted_count = db_table.count - rows_count_before
            logger.info(
                f"Inserted {rows_inserted_count}/{len(articles)} articles from {source}"  # noqa: E501
            )

    db.close()

    time_delta = datetime.now() - start_time
    logger.info(f"Downloading done in {time_delta.total_seconds()}")


if __name__ == "__main__":
    init()
