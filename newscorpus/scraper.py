import datetime
import logging
import time
from copy import deepcopy
from dataclasses import dataclass

import feedparser
from fake_useragent import UserAgent
from pydantic import BaseModel, Field, ValidationError, field_serializer
from trafilatura import bare_extraction, fetch_url
from trafilatura.settings import DEFAULT_CONFIG

from newscorpus import config
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


class Article(BaseModel):
    title: str
    description: str | None = None
    text: str = Field(..., min_length=config.MIN_TEXT_LENGTH)
    url: str
    published_at: datetime.datetime
    source: int

    @field_serializer("published_at")
    def serialize_published_at(self, published_at: datetime.datetime, _info):
        return published_at.timestamp()


# def parse_iso_timestamp(timestamp: str) -> datetime.datetime:
#     """
#     Parse ISO timestamp with local timezone information and
#     return UTC datetime
#     """
#     utc = datetime.timezone.utc
#     return datetime.datetime.fromisoformat(timestamp).astimezone(utc)


def process_feed_item(feed_item: FeedItem, source: Source):
    url = feed_item.link
    raw_text = fetch_url(url, config=TRAFI_CONFIG)

    if not raw_text:
        raise ValueError(f"Could not fetch {url}")

    data = bare_extraction(
        raw_text,
        only_with_metadata=True,
        date_extraction_params={"outputformat": "%Y-%m-%d %H:%M:%S.%f"},
        url=url,
    )

    if not data:
        raise ValueError(f"Could not extract data from {url}")

    article = Article(
        title=data.get("title"),  # or feed_item.title?
        description=data.get("description"),
        text=data.get("text"),
        url=url,
        published_at=datetime.datetime.fromisoformat(data.get("date")),
        source=source.id,
    )

    # date must be withing last n days
    difference = datetime.datetime.now() - article.published_at
    if difference.days > config.KEEP_DAYS:
        raise ValueError(f"Article is too old: {difference.days} days")

    return article


def scrape_source(source: Source):
    articles: list[Article] = []
    logger = logging.getLogger("rotating_log")

    # parse feed
    feed = feedparser.parse(source.url)

    # loop feed entries
    for feed_item in feed.entries:
        try:
            new_article = process_feed_item(feed_item, source)
        except (ValueError, ValidationError) as exc:
            if config.DEBUG:
                logger.error(f"Error processing {feed_item.link}")
                logger.exception(exc, exc_info=False)
            continue
        else:
            articles.append(new_article)

        time.sleep(2)

    logger.info(
        f"Parsed {source.name}, found {len(articles)}/{len(feed.entries)} articles"  # noqa: E501
    )

    return source, articles
