#!/bin/bash

while :
do
  date +%s
  LIMIT=$[ $RANDOM % 10 ]
  curl --stderr - "http://localhost:8001/files/search?pattern=*.txt&&limit=${LIMIT}" | grep -o '\"provider\"......'
  echo "REQ_STATUS=$?"
  sleep 0.1
done
