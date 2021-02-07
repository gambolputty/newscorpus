## Setup
1. Save `.env.example` to `.env` and edit it (see __"Config"__).
2. Run `docker-compose up --build` to create the crawler- and database-container (`-d` to detach the docker process).

## Usage
To start the crawling process run `docker-compose run --rm crawler python -m app crawl` (`-d` to detach the docker process). Ideally execute this command as a cron job.

## Config
Environment variables in `.env`:

| Variable                | Description                                                                                                                        |   |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------|---|
| PYTHON_ENV              | `production` or `development` (verbose logging)                                                                                    |   |
| MONGO_USER              | MongoDB user name                                                                                                                  |   |
| MONGO_PASSWORD          | MongoDB password                                                                                                                   |   |
| MONGO_DB_NAME           | MongoDB database name                                                                                                              |   |
| MONGO_CREATE_TEXT_INDEX | `true` or `1` to let MongoDB create a text index (helpful for [text search](https://docs.mongodb.com/manual/text-search/)) |   |

## Dev setup
1. Save `.env.example` to `.env` and edit it (see "Config").
2. Two options:
  - With VSCode and "Remote-Containers"-Extension: `Remote-Containers: Reopen in Container` or
  - Run `docker-compose -f docker-compose.debug.yml up --build` to create the crawler- and database-container.


## Backup and restore
The are two scripts to backup and restore the MongoDb database:
- `db_backup.sh`
- `db_restore.sh`

Make sure your `.env` file is configured properly and both files are executeable before using them (e.g. `chmod +x db_backup.sh`).