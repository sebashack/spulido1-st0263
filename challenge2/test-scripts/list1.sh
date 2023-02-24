#!/bin/bash

while :
do
  date +%s
  LIMIT=$[ $RANDOM % 100 ]
  curl --stderr - "http://localhost:8001/files/list?limit=${LIMIT}" | grep -o '\"provider\"......'
  echo "REQ_STATUS=$?"
  sleep 0.1
done
