#!/usr/bin/env bash

cmd="$1"

case "$cmd" in
    "train")
        poetry run python train.py
        ;;
    "serve")
        # Ensure the target directory exists
        mkdir -p ./assets/api
        sleep 30
        directory="/opt/ml/model"
        echo "Contents of $directory:"
        echo "$(ls $directory)"

        # Try to copy the model file
        if cp /opt/ml/model/model.pickle ./assets/api/ 2>/dev/null; then
            echo "Model file found and copied."
        else
            echo "Model file not found. Assuming it'll be at app default location."
        fi

        # Start the Uvicorn server
        poetry run python serve.py
        ;;
    *)
        exec "$@"
        ;;
esac
