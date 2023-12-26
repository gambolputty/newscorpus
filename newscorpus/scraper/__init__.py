import datetime
import logging
import time
from copy import deepcopy
from dataclasses import dataclass

import feedparser
from fake_useragent import UserAgent
from pydantic import BaseModel, ValidationError
from trafilatura import bare_extraction, fetch_url
from trafilatura.settings import DEFAULT_CONFIG

from newscorpus.database import Article
from newscorpus.sources import Source

TRAFI_CONFIG = deepcopy(DEFAULT_CONFIG)
TRAFI_CONFIG["DEFAULT"]["USER_AGENTS"] = UserAgent().random


# Feed item type definition
# https://feedparser.readthedocs.io/en/latest/common-rss-elements.html
@dataclass
class FeedItem:
    title: str
    link: str
    description: str
    published: str
    published_parsed: tuple
    id: str


# def parse_iso_timestamp(timestamp: str) -> datetime.datetime:
#     """
#     Parse ISO timestamp with local timezone information and
#     return UTC datetime
#     """
#     utc = datetime.timezone.utc
#     return datetime.datetime.fromisoformat(timestamp).astimezone(utc)


class ScraperConfig(BaseModel):
    DEBUG: bool
    KEEP_DAYS: int
    MIN_TEXT_LENGTH: int


class Scraper:
    def __init__(self, config: ScraperConfig):
        self._config = config
        self._logger = logging.getLogger("rotating_log")

    def process_feed_item(self, feed_item: FeedItem, source: Source):
        url = feed_item.link
        raw_text = fetch_url(url, config=TRAFI_CONFIG)

        if not raw_text:
            raise ValueError("Could not fetch URL.")

        data = bare_extraction(
            raw_text,
            only_with_metadata=True,
            date_extraction_params={"outputformat": "%Y-%m-%d %H:%M:%S.%f"},
            url=url,
        )

        if not data:
            raise ValueError("Could not extract data.")

        # text must be longer than n chars
        text = data.get("text")
        if len(text) < self._config.MIN_TEXT_LENGTH:
            raise ValueError(f"Article is too short: {len(text)} chars")

        # date must be withing last n days
        published_at = datetime.datetime.fromisoformat(data.get("date"))
        difference = datetime.datetime.now() - published_at
        if difference.days > self._config.KEEP_DAYS:
            raise ValueError(f"Article is too old: {difference.days} days")

        # only save description if it's not the start of text
        description = data.get("description")
        if description and description == data.get("text")[: len(description)]:
            description = None

        article = Article(
            title=data.get("title"),  # or feed_item.title?
            description=description,
            text=text,
            url=url,
            published_at=published_at,
            source=source.id,
        )

        return article

    def scrape_source(self, source: Source):
        articles: list[Article] = []

        # parse feed
        feed = feedparser.parse(source.url)

        # loop feed entries
        for feed_item in feed.entries:
            try:
                new_article = self.process_feed_item(feed_item, source)
            except (ValueError, ValidationError) as exc:
                if self._config.DEBUG:
                    self._logger.error(f"Error processing {feed_item.link}")
                    self._logger.exception(exc, exc_info=False)
                continue
            else:
                articles.append(new_article)

            time.sleep(2)

        self._logger.info(
            f"Processed {len(articles)}/{len(feed.entries)} feed items from {source.name}"
        )

        return source, articles
