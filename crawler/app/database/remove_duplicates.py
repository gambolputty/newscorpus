import logging
from tqdm import tqdm
import datetime
from time import time
import itertools
from operator import itemgetter
from pprint import pprint
from textwrap import wrap
# from nltk.stem.snowball import GermanStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from app import config
from app.logger import create_rotating_log
from app.database.create_client import create_client
from app.util import words, get_stopwords


date_now = datetime.datetime.now()
date_from = date_now - datetime.timedelta(days=2)
stopwords = get_stopwords(type='full')
create_rotating_log(config.logs_dir_path.joinpath('remove_duplicates.py.log'))
logger = logging.getLogger('rotating_log')


def add_features(doc):
    text_words = [w for w in words(doc['text']) if w.lower() not in stopwords]
    doc['features'] = ' '.join(text_words)
    return doc


def find_duplicates_in_docs(docs):
    # calculate document similarity and compare
    # save newest article, discard older duplicate
    duplicate_docs = {}
    # stemmer = GermanStemmer()
    vectorizer = TfidfVectorizer()
    docs.sort(key=itemgetter('created_at'))

    # loop docs
    for doc in docs:
        if doc['_id'] in duplicate_docs: continue

        for doc_compare in docs:
            if doc == doc_compare: continue
            if doc_compare['_id'] in duplicate_docs: continue

            tfidf = vectorizer.fit_transform([doc['features'], doc_compare['features']])
            similarity = ((tfidf * tfidf.T).A)[0, 1]

            if similarity < .9:
                continue

            # keep oldest
            doc_list = [doc, doc_compare]
            datetime_list = [doc_list[0]['created_at'], doc_list[1]['created_at']]
            oldest = max(datetime_list)
            # youngest = min(datetime_list)
            # original = next((doc for doc in doc_list if doc['created_at'] == youngest), doc)
            duplicate = next((doc for doc in doc_list if doc['created_at'] == oldest), doc_compare)

            if duplicate['_id'] not in duplicate_docs:
                duplicate_docs[duplicate['_id']] = duplicate
                if config.env == 'development':
                    print_articles(similarity, doc, doc_compare)

    return list(duplicate_docs.keys())


def print_articles(similarity, doc, doc_compare):
    for dd in [doc, doc_compare]:
        if dd == doc:
            print(f'Duplicate ({dd["src"]}):')
        else:
            print(f'Original ({dd["src"]}):')

        print(dd['title'])
        print(dd['_id'])
        print(dd['url'])
        print(dd['published_at'])
        print()
        print('\n'.join(wrap(dd['text'][:150].replace(r'\n', ' '), width=50)))
        if dd == doc:
            print()
            print('v'*50)
        print()
    print(f'Similarity: {similarity}')
    print()
    print('*'*85)
    print()
    print('='*100)


def remove_duplicates():
    ts = time()
    logger.info('Removing duplicates.')
    logger.info(f'Loading documents from database from {date_from} - {date_now}')
    [client, db] = create_client()

    # create params
    # query database for docs
    # get docs from date_now to last 24hrs by created_at
    params = {
        'created_at': {
            '$gte': date_from,
            '$lt': date_now
        }
    }
    docs = [add_features(doc) for doc in tqdm(db.articles.find(params), disable=__name__ != '__main__')]

    # Sort by src key
    docs = sorted(docs, key=itemgetter('src'))

    # group docs by source
    logger.debug('Group docs by source')
    for key, group in itertools.groupby(docs, key=itemgetter('src')):
        group = list(group)

        # find duplicates in group
        ids_to_remove = find_duplicates_in_docs(group)
        if not ids_to_remove:
            continue

        # remove from database
        try:
            db.articles.remove({'_id': { '$in': ids_to_remove } })
            logger.info(f'Removed {len(ids_to_remove)} duplicates in source {key}')
        except Exception as e:
            logger.exception(e)

    # close connection to db client
    client.close()

    logger.info(f'Removing duplicates done in {time() - ts}')
