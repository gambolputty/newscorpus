import datetime
from pathlib import Path

from tqdm import tqdm

from newscorpus.database import Article, Database


def import_articles_from_json(json_file_path: Path):
    """
    Import articles from old MongoDB json file.

    To execute:
        poetry run python -c "from newscorpus.database.migration_scripts import import_articles_from_json; import_articles_from_json('/path-tp/articles.json')"
    """
    import json

    db = Database()
    db._db.execute("PRAGMA synchronous = OFF")
    db._db.execute("PRAGMA journal_mode = MEMORY")

    # Begin a transaction
    db._db.execute("BEGIN")

    with open(json_file_path, "r") as f:
        try:
            for line in tqdm(f):
                old_article = json.loads(line)
                published_at = datetime.datetime.fromisoformat(
                    old_article["published_at"]["$date"]
                )

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


def import_with_url_check_articles_from_json(json_file_path: Path):
    """
    Import articles from old MongoDB json file
    """
    import json

    from dateparser import parse

    db = Database()
    articles = []

    with open(json_file_path, "r") as f:
        for line in tqdm(f):
            old_article = json.loads(line)
            published_at = parse(old_article["published_at"]["$date"])

            if not published_at:
                print("Could not parse date")
                continue

            # skip articles older than n days
            difference = datetime.datetime.now() - published_at
            if difference.days > 14:
                continue

            new_article = Article(
                title=old_article["title"],
                description=None,
                text=old_article["text"],
                url=old_article["url"],
                published_at=published_at,
                source=old_article["src"],
            )
            articles.append(new_article.model_dump())

    db.insert_articles(articles)

    db.close()
