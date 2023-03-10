#!/bin/bash

set -xeuf -o pipefail

# Install Python deps
sudo apt install -y python3 python3-venv python3-pip build-essential curl git
python3 -m pip install --upgrade pip

# Install docker
if ! type "docker" > /dev/null; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update

    apt-cache policy docker-ce

    if [[ -v CI ]]; then
        echo "Skipping creation of docker group"
    else
        sudo apt install -y docker-ce
        sudo usermod -aG docker ${USER}
    fi
else
    echo 'docker already installed'
fi

# Install docker-compose
if ! type "docker-compose" > /dev/null; then
    sudo curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo 'docker-compose already installed'
fi
