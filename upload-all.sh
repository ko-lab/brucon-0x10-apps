#!/bin/bash

for dir in apps/*; do
  echo "doing upload.sh for dir [$dir]"
  ./upload-one.sh $dir
done
