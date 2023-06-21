#!/usr/bin/env bash

mkdir -p ./staging
chmod 700 ./staging

# assign ID if provided, otherwise generate one
ID=${1:-$(uuidgen)}

echo "ID ${ID}"

mkdir -p "./secrets/${ID}"
chmod 700 "./secrets/${ID}"

mv ./staging/* "./secrets/${ID}/"
chmod 600 "./secrets/${ID}/*"
