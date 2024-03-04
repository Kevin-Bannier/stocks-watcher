#!/bin/bash
set -e

MONGO_NAME="mongodb"
MONGO_PORT=27017

START=false
STOP=false

if [[ "$1" == "start" ]]; then
  START=true
elif [[ "$1" == "stop" ]]; then
  STOP=true
else
  exit 1
fi

# echo "$START"
# echo "$STOP"


if [[ "$START" == "true" ]]; then
  echo "Starting..."
  docker pull mongo:latest
  docker run -d -p 27017:27017 --name=${MONGO_NAME} mongo:latest
  echo "MongoDB serevr started at: 127.0.0.1:${MONGO_PORT}"
fi

if [[ "$STOP" == "true" ]]; then
  echo "Stoping..."
  docker stop ${MONGO_NAME}
  docker rm ${MONGO_NAME}
fi
