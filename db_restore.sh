#!/bin/bash
set -e

# to make this script executeable: chmod +x restore_db.sh

CONTAINER_NAME=newscorpus_mongo
DUMP_FILE_PATH=newscorpus.dump

echo "Restoring database, dropping collections first..."

# load .env variables
export $(grep -v '^#' .env | xargs)

docker exec -i $CONTAINER_NAME sh -c "mongorestore -u ${MONGO_USER} -p ${MONGO_PASSWORD} --archive --drop --authenticationDatabase admin" < $DUMP_FILE_PATH
