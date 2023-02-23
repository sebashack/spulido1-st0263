#!/bin/bash

set -xeuf -o pipefail

ROOT="$( readlink -f "$( dirname "${BASH_SOURCE[0]}" )" )"
DOCKER_FILE="${ROOT}/docker-compose.yaml"
RABBIT_DIR="${ROOT}/rabbit"

export RABBIT_HOME_DIR="${RABBIT_DIR}/home"

if [[ $1 == "up" ]]; then
    docker-compose --file "$DOCKER_FILE" up --detach
fi

if [[ $1 == "down" ]]; then
    docker-compose --file "$DOCKER_FILE" down
fi
