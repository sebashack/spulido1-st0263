#!/bin/bash

while :
do
  date +%s
  curl --stderr - "http://localhost:8001/files/list" | grep -o '\"provider\"......'
  echo "REQ_STATUS=$?"
  sleep 0.5
done
