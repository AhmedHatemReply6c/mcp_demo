#!/bin/sh

# Read models from env var
MODELS=${PREPULL_MODELS:-$(tr '\n' ' ' < /models.txt)}

# Fail if no models specified
[ -z "$MODELS" ] && exit 1

# Loop through each model and check if it's present in ollama list
for model in $MODELS; do
    if ! ollama list | grep -q "$model"; then
        echo "Model $model not found"
        exit 1
    fi
done

# All models found
exit 0
