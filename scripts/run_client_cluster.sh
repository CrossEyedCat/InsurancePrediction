#!/bin/bash
# Script to run Flower client on Hackathon cluster
# Usage: ./run_client_cluster.sh <client_id> <server_address>
# Example: ./run_client_cluster.sh 1 localhost:8080

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <client_id> <server_address>"
    echo "Example: $0 1 localhost:8080"
    exit 1
fi

CLIENT_ID=$1
SERVER_ADDRESS=$2

cd ~

export FLOWER_SERVER_URL="$SERVER_ADDRESS"
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"

echo "Starting Flower Client $CLIENT_ID"
echo "Connecting to server: $SERVER_ADDRESS"

python flower_client/client.py --client-id $CLIENT_ID --server-address $SERVER_ADDRESS --data-dir output


