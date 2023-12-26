# Newscorpus 📰🐍
<!-- Description of this project -->
Takes a list of RSS feeds, downloads and processes new articles and stores the result in a SQLite database.

This project uses [Trafilatura](https://github.com/adbar/trafilatura) to extract text from HTML pages and [feedparser](https://github.com/kurtmckee/feedparser) to parse RSS feeds.


## Setup
This project uses [Poetry](https://python-poetry.org/) to manage dependencies. Make sure you have it installed.
```bash
# Clone this repository
git clone git@github.com:gambolputty/newscorpus.git

# Install dependencies with poetry
cd newscorpus
poetry install
```

## Usage
To start the scraping process run:

`poetry run scrape`

There are some optional arguments:

## Configuration

| Option             | Default                           | Description                                                                                                                        |
|--------------------|-----------------------------------|------------------------------------------------------------------------------|
| --src-path         | [`newscorpus/sources/sources.json`](newscorpus/sources/sources.json) | Path to a `sources.json`-file.            |
| --db-path          | `newscorpus.db`                   | Path to the SQLite database to use.                                          |
| --debug            | _none_ (flag)                     | Show debug information.                                                      |
| --workers          | `4`                               | Number of download workers.                                                  |
| --keep             | `2`                               | Don't save articles older than n days.                                       |
| --min-length       | `350`                             | Don't process articles with a text length smaller than x characters.         |
| --help             | _none_ (flag)                     | Show help menu.                                                              |

## Acknowledgements
- [IFG-Ticker](https://github.com/beyondopen/ifg-ticker) for some source

## License
[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE)