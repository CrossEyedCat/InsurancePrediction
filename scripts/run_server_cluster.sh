#!/bin/bash
# Script to run Flower server on Hackathon cluster
# This should be submitted as a job via submit-job.sh

cd ~

export SERVER_ADDRESS="0.0.0.0"
export SERVER_PORT="8080"
export NUM_ROUNDS="10"
export MIN_CLIENTS="3"
export FRACTION_FIT="1.0"
export FRACTION_EVALUATE="1.0"
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"

echo "Starting Flower Server..."
echo "Server will listen on port $SERVER_PORT"
echo "Waiting for 3 clients to connect..."

python flower_server/server.py


