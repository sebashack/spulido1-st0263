#!/bin/bash

set -xeuf -o pipefail

ROOT="$( readlink -f "$( dirname "${BASH_SOURCE[0]}" )" )"
DOCKER_FILE="${ROOT}/docker-compose.yaml"

export NGINX_CONFIG_DIR="${ROOT}/config"
export WORDPRESS_DIR="/mnt/wordpress"
export LETSENCRYPT_DIR="/etc/letsencrypt"

if [[ $1 == "up" ]]; then
    docker-compose --file "$DOCKER_FILE" up --detach
elif [[ $1 == "down" ]]; then
    docker-compose --file "$DOCKER_FILE" down
else
    echo "Invalid option. Pick out one of [up, down]"
    exit 1
fi
