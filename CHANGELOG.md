# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2023-12-27
### Changed
- Provide example sources.example.json file

### Added
- Add database method `iter_articles` to iterate over all articles in the database

### Removed
- Remove default sources.json file

## [2.0.0] - 2023-12-27
### Changed
- Remove Docker setup and use Poetry for dependencies
- Replace MongoDB with SQLite

### Added
- Optional CLI arguments

## [1.2.1] - 2021-03-14
### Added
- Set `--wiredTigerCacheSizeGB` flag to limit memory consumption of MongoDB

## [1.2.0] - 2021-02-12
### Added
- Shell script that executes the crawl command
### Changed
- Directory structure
- Simplified crawl command

## [1.1.0] - 2021-02-11
### Added
- Three new config variables (`MONGO_OUTSIDE_PORT`, `MAX_WORKERS`, `KEEP_DAYS`). See [readme](README.md) for details.
- Network name for this project (`network name`)
- Changelog file
### Changed
- Config variables are now uppercase
- Readme

## [1.0.0] - 2021-02-07
### Added
- Initial project release