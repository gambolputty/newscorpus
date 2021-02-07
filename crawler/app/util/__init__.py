import re
from pathlib import Path
from app import config

def words(text, lower=False):
    words = re.findall(r'[\wÜüÖöÄäß]+', text)
    if lower is True:
        return [w.lower() for w in words]
    return words


def get_stopwords(type='plain'):
    # compare lists: http://jura.wi.mit.edu/cgi-bin/bioc/tools/compare.cgi
    if type in ['full', 'plain']:
        filepath = config.assets_dir_path.joinpath(f'german_stopwords_{type}.txt')
        with open(filepath, encoding='utf-8') as f:
            return f.read().split('\n')