#!/bin/bash
set -e

# to make this script executeable: chmod +x restore_db.sh

CONTAINER_NAME=newscorpus_mongo
DUMP_FILE_PATH=newscorpus.dump

echo "Creating database backup..."

# load .env variables
export $(grep -v '^#' .env | xargs)

docker exec $CONTAINER_NAME sh -c "mongodump -d newscorpus -u ${MONGO_USER} -p ${MONGO_PASSWORD} --archive --authenticationDatabase admin" > $DUMP_FILE_PATH
