# Newscorpus 📰🐳🐍
Docker setup for automated news article crawling from German news websites (~60 sources, see [sources.json](crawler/app/assets/sources.json)).
Written in Python, uses [Newspaper](https://pypi.org/project/newspaper3k/) as a content extractor and MongoDB as database.

Development environment is ready to be used with [VSCode](https://code.visualstudio.com/docs/remote/containers) and the [Remote Container Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

## Setup
1. Clone this repository `git clone git@github.com:gambolputty/newscorpus.git && cd newscorpus`
2. Save `.env.example` to `.env` and edit it (see __"Configuration"__).
3. Run `docker-compose up --build` to create the crawler- and database-container (`-d` to detach the docker process).

## Usage
To start the crawling process run:

`docker-compose run --rm crawler ./crawl.sh`

Add `-d` after `--rm` to detach the docker process. Ideally execute this command as a cron job.

## Configuration
Environment variables in `.env`:

| Variable                | Description                                                                                                                        |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| PYTHON_ENV              | `production` or `development` (verbose logging)                                                                                    |
| MONGO_USER              | MongoDB user name                                                                                                                  |
| MONGO_PASSWORD          | MongoDB password                                                                                                                   |
| MONGO_DB_NAME           | MongoDB database name                                                                                                              |
| MONGO_CREATE_TEXT_INDEX | `true` or `1` to let MongoDB create a text index (helpful for [text search](https://docs.mongodb.com/manual/text-search/))         |
| MONGO_OUTSIDE_PORT      | Exposed MongoDB port, accessible on your host machine.                                                                                         |
| MAX_WORKERS             | Number of worker threads for the crawler. Remove for auto assignment.                                                         |
| KEEP_DAYS               | Discard articles older than **n** days. Default is "2".                                                                            |

At the moment, there are no other options. If you want to change the sources being crawled, take a look at [sources.json](crawler/app/assets/sources.json).

## Dev setup
1. Save `.env.example` to `.env` and edit it (see "Config").
2. Two options:
  - With VSCode and "Remote-Containers"-Extension: `Remote-Containers: Reopen in Container` ([working inside a Docker container](https://code.visualstudio.com/docs/remote/containers))
  - Without VSCoce: run `docker-compose -f docker-compose.debug.yml up --build` to create the crawler- and database-container.


## Database backup and restore
The database volume is mapped to a folder named `mongo_data` which is located in the root of this project.
The are two scripts to backup and restore the database:
- `db_backup.sh`
- `db_restore.sh` (be aware that this will drop all collections first)

Make sure your `.env` file is configured properly and both files are executeable before using them (e.g. `chmod +x db_backup.sh`).


## Example database document (with MongoDB fields):

```json
{
  "_id": {
    "$oid": "5e0ec55caf879ef7de34682d"
  },
  "title": "Sudan: 18 Tote bei Absturz von Lazarettmaschine",
  "published_at": {
    "$date": "2020-01-02T21:06:08.000Z"
  },
  "created_at": {
    "$date": "2020-01-03T05:38:37.541Z"
  },
  "url": "https://www.sueddeutsche.de/politik/sudan-flugzeugabsturz-roter-halbmond-1.4743878",
  "src": 4,
  "text": "Nach Angaben der Hilfsorganisation Roter Halbmond sollte das Flugzeug Patienten in die Hauptstadt fliegen. Die Menschen waren bei heftigen Kämpfen verletzt worden.\n\nIm Sudan sind beim Absturz einer Lazarettmaschine des Militärs nach offiziellen Angaben alle 18 Menschen an Bord ums Leben gekommen. Bei den Toten handele es sich um sieben Besatzungsmitglieder, drei Richter und acht weitere Zivilisten, teilt der Sprecher des Militärs, General Amer Muhammad Al-Hassan, mit.\n\nDas Flugzeug vom Typ Antonow habe fünf Minuten nach dem Start vom Flughafen der Stadt El Geneina im Westen des Landes aus unbekannter Ursache an Höhe verloren und sei am Boden zerschellt. Ihr Ziel war Khartum, die Hauptstadt des ostafrikanischen Landes.\n\nDas Flugzeug sollte nach Angaben der sudanesischen Hilfsorganisation Roter Halbmond Patienten zur Behandlung in die Hauptstadt fliegen. Die Menschen seien in den vergangenen Tagen bei heftigen Kämpfen in den vergangenen Tagen zwischen rivalisierenden Volksgruppen in Darfur verletzt worden. Dabei habe es nach Angaben des Roten Halbmondes insgesamt 48 Tote und Dutzende Verletzte gegeben.\n\nIn Darfur an der Grenze zum Tschad kämpfen Rebellen seit mehr als einem Jahrzehnt gegen Truppen der Zentralregierung und mit ihnen verbündete lokale arabische Milizen."
}
```

## Acknowledgements
- [IFG-Ticker](https://github.com/beyondopen/ifg-ticker) for some source

## License
[GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE)