import sys
from pathlib import Path


if len(sys.argv) <= 1:
    print('No arguments provided')
    sys.exit()


# add current diretory path to python path to execute "app" from any location
sys.path.append(Path.cwd().as_posix())

# parse args
cmd = sys.argv[1]

# process args
if cmd == 'crawl':
    from app import crawler
    crawler.init()
# elif cmd == 'dups':
#     from .database.remove_duplicates import remove_duplicates
#     remove_duplicates()
