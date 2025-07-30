#!/usr/bin/env bash
set -euo pipefail

ollama serve &
SERVER_PID=$!


while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

MODELS=${PREPULL_MODELS:-$(tr '\n' ' ' < /models.txt)}

echo "[entrypoint] Pre-pulling models: $MODELS"

for M in $MODELS; do
  if ! ollama list | grep -q "$M"; then
    echo "→ pulling $M"
    ollama pull "$M"
  else
    echo "✔ $M already in cache"
  fi
done

echo "[entrypoint] All models ready."
wait "$SERVER_PID"