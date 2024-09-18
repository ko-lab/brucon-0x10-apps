#!/bin/bash
PORT=$1
for dir in apps/*; do
  echo "doing upload.sh for dir [$dir] to port $PORT"
  ./upload-one.sh $dir $PORT
done
./connect.sh $PORT reset
