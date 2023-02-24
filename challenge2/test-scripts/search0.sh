#!/bin/bash

while :
do
  date +%s
  curl --stderr - "http://localhost:8001/files/search?pattern=*.txt" | grep -o '\"provider\"......'
  echo "REQ_STATUS=$?"
  sleep 0.1
done
