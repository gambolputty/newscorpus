from pymongo import MongoClient, DESCENDING, TEXT

from app import config


def create_client():
    client = MongoClient(config.MONGO_HOST, config.MONGO_PORT,
                         username=config.MONGO_USERNAME, password=config.MONGO_PASSWORD)

    db = client[config.MONGO_DB_NAME]

    # create indexes
    db.articles.create_index('url', unique=True)
    db.articles.create_index([('created_at', DESCENDING)])

    if config.MONGO_CREATE_TEXT_INDEX is True:
        db.articles.create_index([('text', TEXT)], default_language='german')

    return [client, db]
