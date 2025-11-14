#!/bin/bash
# Start Flower client
# Usage: ./start_client.sh <client_id>

if [ -z "$1" ]; then
    echo "Usage: $0 <client_id>"
    echo "Example: $0 1"
    exit 1
fi

CLIENT_ID=$1

cd "$(dirname "$0")/.."

export FLOWER_SERVER_URL="localhost:8080"
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"

python flower_client/client.py --client-id $CLIENT_ID --server-address localhost:8080 --data-dir output


