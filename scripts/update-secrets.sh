#!/usr/bin/env bash

SIGNATURE_FILE=$(mktemp) || exit 1
FETCHED_FILE=$(mktemp) || exit 1

# Cleanup when the script exits
# http://redsymbol.net/articles/bash-exit-traps/
function cleanup () {
  rm "$SIGNATURE_FILE" "$FETCHED_FILE" 
}
trap finish EXIT

curl -s -F "key=@${HOST_PUBLIC_KEY_PATH:?}" -X POST "https://${MIMI_DOMAIN:?}/sign/${NODE_ID:?}" -o "$SIGNATURE_FILE"
curl -s -F "key=@${HOST_PUBLIC_KEY_PATH:?}" -X POST "https://${MIMI_DOMAIN:?}/get/${NODE_ID:?}" | rage --decrypt -i "${HOST_KEY_PATH:?}" -o "$FETCHED_FILE"
if ssh-keygen -Y check-novalidate -n file -f "${PROVISIONER_PUBLIC_KEY:?}" -s "$SIGNATURE_FILE" < "$FETCHED_FILE"; then
  echo "Signature is valid."
else
  echo "Signature is invalid."
  exit 1
fi
mkdir -p /etc/mimi-secrets/
chmod 700 /etc/mimi-secrets/
tar -xzf "$FETCHED_FILE" -C /etc/mimi-secrets/ --overwrite-dir --recursive-unlink --mode "o=rwx"
