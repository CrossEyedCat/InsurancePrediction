#!/bin/bash
# All-in-one script to run federated learning on cluster
# This runs server and all 3 clients in the same job

cd ~

echo "=========================================="
echo "Starting Federated Learning"
echo "=========================================="

# Configuration
export SERVER_ADDRESS="0.0.0.0"
export SERVER_PORT="8080"
export NUM_ROUNDS="10"
export MIN_CLIENTS="3"
export FRACTION_FIT="1.0"
export FRACTION_EVALUATE="1.0"
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"

# Check if data exists
if [ ! -d "output" ]; then
    echo "Error: output directory not found!"
    echo "Please extract federated_learning.tar.gz first"
    exit 1
fi

# Start server in background
echo "Starting server..."
python flower_server/server.py > server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 10

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Server failed to start!"
    cat server.log
    exit 1
fi

echo "Server started (PID: $SERVER_PID)"
echo "Starting clients..."

# Start clients in background
for i in 1 2 3; do
    echo "Starting client $i..."
    python flower_client/client.py --client-id $i --server-address localhost:8080 --data-dir output > client_$i.log 2>&1 &
    CLIENT_PIDS[$i]=$!
    sleep 2
done

echo "All processes started!"
echo "Server PID: $SERVER_PID"
echo "Client PIDs: ${CLIENT_PIDS[1]} ${CLIENT_PIDS[2]} ${CLIENT_PIDS[3]}"
echo ""
echo "Monitoring logs (Ctrl+C to stop)..."
echo ""

# Monitor logs
tail -f server.log client_*.log &
TAIL_PID=$!

# Wait for server to complete
wait $SERVER_PID
SERVER_EXIT=$?

# Stop tail
kill $TAIL_PID 2>/dev/null

# Stop clients
for pid in ${CLIENT_PIDS[@]}; do
    kill $pid 2>/dev/null
done

echo ""
echo "=========================================="
echo "Training completed!"
echo "=========================================="
echo "Server exit code: $SERVER_EXIT"
echo ""
echo "Check logs:"
echo "  - Server: server.log"
echo "  - Clients: client_1.log, client_2.log, client_3.log"
echo ""
echo "Check models:"
echo "  ls -lh flower_server/models/"

exit $SERVER_EXIT


