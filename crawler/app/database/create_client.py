from pymongo import MongoClient, DESCENDING, TEXT

from app import config


def create_client():
    client = MongoClient(config.mongo_host, config.mongo_port,
                         username=config.mongo_username, password=config.mongo_password)

    db = client[config.mongo_dbname]

    # create indexes
    db.articles.create_index('url', unique=True)
    db.articles.create_index([('created_at', DESCENDING)])

    if config.create_mongo_text_index is True:
        db.articles.create_index([('text', TEXT)], default_language='german')

    return [client, db]
