import json
from time import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dateutil.parser import parse as parseDate
from dateutil.parser import ParserError
import feedparser
import newspaper
from newspaper import Article, Config
from pymongo.errors import BulkWriteError

from app.logger import create_rotating_log
from app import config
from app.database.create_client import create_client
from app.random_user_agent import random_user_agent


create_rotating_log(config.LOGS_PATH.joinpath("crawlerlog"))
logger = logging.getLogger("rotating_log")

MIN_TEXT_LENGTH = 350


def init():
    ts = time()
    logger.info('Downloading new articles')
    logger.info(f'Ignoring articles older than {config.KEEP_DAYS} days')

    if config.MAX_WORKERS:
        logger.info(f'Maximum crawler workers: {config.MAX_WORKERS}')

    # load sources
    with open(config.SOURCES_PATH, encoding='utf-8') as f:
        sources = json.load(f)

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        executor.map(scrape_source, sources)

    logger.info(f"Downloading done in {time() - ts}")


def create_newspaper_config():
    newspaper_config = Config()
    newspaper_config.browser_user_agent = random_user_agent()
    newspaper_config.language = 'de'

    return newspaper_config


def process_feed_item(feed_item, source, articles_in_memory, db):
    # check for duplicate in db
    if db.articles.find_one({'url': feed_item.link}) is not None:
        logger.debug('Skip: article already exists')
        return False

    # check if link exists already in memory
    if any(a['url'] == feed_item.link for a in articles_in_memory):
        logger.debug('Skip: article already exists')
        return False

    # parse article
    try:
        article = Article(feed_item.link, config=create_newspaper_config())
        article.download()
        article.parse()
    except newspaper.article.ArticleException as exc:
        logger.debug(f'Newspaper error: {exc}')
        # logger.exception(exc)
        return False

    # check title
    article_title = article.title.strip()
    if not article_title:
        logger.debug('Skip: no title or text')
        return False

    # check text
    article_text = article.text.strip()
    if len(article_text) < MIN_TEXT_LENGTH:
        logger.debug('Skip: text too short')
        return False

    # must have date
    published_at_val = None
    if article.publish_date:
        # get from parsed article
        published_at_val = article.publish_date
    elif hasattr(feed_item, 'published'):
        # get from feed item
        published_at_val = feed_item.published

    if not published_at_val:
        logger.debug('Skip: missing date')
        return False

    # normalize date, create datetime object, remove time zone
    if isinstance(published_at_val, datetime):
        published_at = published_at_val.replace(tzinfo=None)
    elif isinstance(published_at_val, str):
        try:
            published_at = parseDate(published_at_val, ignoretz=True)
        except ParserError as exc:
            logger.debug(f'Dateutil parse error: {exc}')
            return False
    else:
        logger.debug('No valid date found')
        return False

    # date must be withing last n days
    difference = datetime.now() - published_at
    if difference.days > config.KEEP_DAYS:
        logger.debug(
            f'Skip: Article older than {config.KEEP_DAYS} days ({published_at})'
        )
        return False

    # create mew item
    return {
        'title': article_title,
        'published_at': published_at,
        'created_at': datetime.now(),
        'url': feed_item.link,
        'src': source['id'],
        'text': article_text
    }


def scrape_source(source):
    [client, db] = create_client()  # pyMongo not thread safe
    articles = []

    # loop feed
    feed = feedparser.parse(source['url'])
    logger.info(
        f'Parsing: {source["name"]} (id: {source["id"]}), count: {len(feed.entries)}'
    )

    # process feed items
    # download article & create database document
    for feed_item in feed.entries:
        new_article = process_feed_item(feed_item, source, articles, db)

        if not new_article:
            continue

        articles.append(new_article)

    # save articles to db
    if articles:
        try:
            response = db.articles.insert_many(articles)
            logger.info(
                f'Saved {len(response.inserted_ids)} article(s) from {source["name"]} to database'
            )
        except BulkWriteError as bwe:
            logger.exception(bwe)
            logger.error(bwe.details)
            # you can also take this component and do more analysis
            # werrors = bwe.details['writeErrors']
            # raise
    else:
        logger.info(f'No new articles found in {source["name"]}')

    # close connection to db client
    client.close()


if __name__ == "__main__":
    init()
