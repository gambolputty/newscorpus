from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import click

from newscorpus.database import Database
from newscorpus.logger import create_rotating_log
from newscorpus.scraper import Scraper, ScraperConfig
from newscorpus.sources import SourceCollection


@click.command()
@click.option(
    "--src-path",
    type=str,
    help="Path to a sources.json file",
)
@click.option(
    "--db-path",
    type=str,
    help="Path to a SQLite database file",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
@click.option(
    "--workers",
    type=int,
    help="Maximum number of workers",
    default=4,
)
@click.option(
    "--keep",
    type=int,
    help="Don't save articles older than n days",
    default=2,
)
@click.option(
    "--min-length",
    type=int,
    help="Minimum text length",
    default=350,
)
def init(
    src_path: str | None,
    db_path: str | None,
    debug: bool,
    workers: int,
    keep: int,
    min_length: int,
):
    start_time = datetime.now()
    logger = create_rotating_log(debug)
    logger.info("Downloading new articles")
    logger.info(f"Ignoring articles older than {keep} days")
    logger.info(f"Maximum number of workers: {workers}")

    sources = SourceCollection.from_file(src_path).root
    db = Database(db_path)
    scraper = Scraper(
        ScraperConfig(
            DEBUG=debug,
            KEEP_DAYS=keep,
            MIN_TEXT_LENGTH=min_length,
        )
    )

    # scrape sources
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for source, articles in executor.map(scraper.scrape_source, sources):
            # Convert articles to dictionaries
            articles_dumped = [article.model_dump() for article in articles]

            # Insert into database
            insert_count = db.insert_articles(articles_dumped)

            logger.info(
                f"Inserted {insert_count}/{len(articles)} articles from {source.name}"
            )

    db.close()

    time_delta = datetime.now() - start_time
    logger.info(f"Downloading done in {time_delta.total_seconds()} seconds")


if __name__ == "__main__":
    init()
