#!/bin/bash

sudo mkdir -p /mnt/wordpress
sudo mount -v -t nfs 10.128.0.5:/var/mnt/wordpress /mnt/wordpress
