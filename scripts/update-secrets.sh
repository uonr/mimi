#!/usr/bin/env bash

SIGNATURE_FILE=$(mktemp)
FETCHED_FILE=$(mktemp)

curl -s -F "key=@${HOST_PUBLIC_KEY_PATH:?}" -X POST "https://${MIMI_DOMAIN:?}/sign/$(hostname)" -o "$SIGNATURE_FILE"
curl -s -F "key=@${HOST_PUBLIC_KEY_PATH:?}" -X POST "https://${MIMI_DOMAIN:?}/get/$(hostname)" | rage --decrypt -i "${HOST_KEY_PATH:?}" -o "$FETCHED_FILE"
if ssh-keygen -Y check-novalidate -n file -f "${PROVISIONER_PUBLIC_KEY:?}" -s "$SIGNATURE_FILE" < "$FETCHED_FILE"; then
  echo "Signature is valid."
else
  echo "Signature is invalid."
  rm "$SIGNATURE_FILE" "$FETCHED_FILE"
  exit 1
fi
mkdir -p /etc/mimi-secrets/
chmod 700 /etc/mimi-secrets/
tar -xzf "$FETCHED_FILE" -C /etc/mimi-secrets/ --overwrite-dir --recursive-unlink --mode "o=rwx"
rm "$SIGNATURE_FILE" "$FETCHED_FILE"
