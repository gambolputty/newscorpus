# Newscorpus 📰🐍
<!-- Description of this project -->
Takes a list of RSS feeds, downloads found articles, processes them and stores the result in a SQLite database.

This project uses [Trafilatura](https://github.com/adbar/trafilatura) to extract text from HTML pages and [feedparser](https://github.com/kurtmckee/feedparser) to parse RSS feeds.


## Installation
This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Make sure you have it installed.

### Via Poetry
```bash
poetry add "git+https://github.com/gambolputty/newscorpus.git"
```

### Via clone
```bash
# Clone this repository
git clone git@github.com:gambolputty/newscorpus.git

# Install dependencies with poetry
cd newscorpus
poetry install
```

## Configuration
Copy the [example sources file](sources.example.json) and edit it to your liking.
```bash
cp sources.example.json sources.json
```
It is expected to be in the following format:
```json
[
  {
    "id": 0,
    "name": "Example",
    "url": "https://example.com/rss",
  },
  ...
]
```

## Usage

### Starting the scraper (CLI)
To start the scraping process run:
```bash
poetry run scrape [OPTIONS]
```

#### Options (optional)

| Option             | Default                           | Description                                                                                                                        |
|--------------------|-----------------------------------|------------------------------------------------------------------------------|
| --src-path         | `sources.json`                    | Path to a `sources.json`-file.            |
| --db-path          | `newscorpus.db`                   | Path to the SQLite database to use.                                          |
| --debug            | _none_ (flag)                     | Show debug information.                                                      |
| --workers          | `4`                               | Number of download workers.                                                  |
| --keep             | `2`                               | Don't save articles older than n days.                                       |
| --min-length       | `350`                             | Don't process articles with a text length smaller than x characters.         |
| --help             | _none_ (flag)                     | Show help menu.                                                              |

### Accessing the database
Access the database within your Python script:
```python
from newscorpus import Database

db = Database()

for article in db.iter_articles():
    print(article.title)
    print(article.published_at)
    print(article.text)
    print()
```
Arguments to `iter_articles()` are the same as for `rows_where()`in [sqlite-utils](https://sqlite-utils.datasette.io/) ([Docs](https://sqlite-utils.datasette.io/en/stable/python-api.html#listing-rows), [Reference](https://sqlite-utils.datasette.io/en/stable/reference.html#sqlite_utils.db.Queryable.rows_where)).

The `Database` class takes an optional `path` argument to specify the path to the database file.

## Acknowledgements
- [IFG-Ticker](https://github.com/beyondopen/ifg-ticker) for some source

## License
[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE)