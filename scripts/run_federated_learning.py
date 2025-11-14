"""
Script to run federated learning with Flower
Starts 1 server and 3 clients
"""
import subprocess
import sys
import time
import os
from pathlib import Path

# Configuration
SERVER_ADDRESS = "localhost"
SERVER_PORT = "8080"
NUM_CLIENTS = 3
DATA_DIR = "output"

def start_server():
    """Start Flower server"""
    print("=" * 60)
    print("Starting Flower Server")
    print("=" * 60)
    
    server_script = Path(__file__).parent.parent / "flower_server" / "server.py"
    
    env = os.environ.copy()
    env["SERVER_ADDRESS"] = SERVER_ADDRESS
    env["SERVER_PORT"] = SERVER_PORT
    env["NUM_ROUNDS"] = "10"
    env["MIN_CLIENTS"] = "3"
    env["FRACTION_FIT"] = "1.0"
    env["FRACTION_EVALUATE"] = "1.0"
    env["LOCAL_EPOCHS"] = "5"
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"Server started with PID: {process.pid}")
    return process

def start_client(client_id):
    """Start Flower client"""
    print(f"\nStarting Client {client_id}")
    
    client_script = Path(__file__).parent.parent / "flower_client" / "client.py"
    
    env = os.environ.copy()
    env["FLOWER_SERVER_URL"] = f"{SERVER_ADDRESS}:{SERVER_PORT}"
    env["LOCAL_EPOCHS"] = "5"
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    
    process = subprocess.Popen(
        [sys.executable, str(client_script), 
         "--client-id", str(client_id),
         "--server-address", f"{SERVER_ADDRESS}:{SERVER_PORT}",
         "--data-dir", DATA_DIR],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"Client {client_id} started with PID: {process.pid}")
    return process

def main():
    """Main function"""
    print("=" * 60)
    print("Federated Learning Setup")
    print("=" * 60)
    print(f"Server: {SERVER_ADDRESS}:{SERVER_PORT}")
    print(f"Clients: {NUM_CLIENTS}")
    print(f"Data directory: {DATA_DIR}")
    print()
    
    # Check if data directory exists
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        print(f"Error: Data directory '{DATA_DIR}' not found!")
        print("Please run the data generation scripts first.")
        return
    
    # Start server
    server_process = start_server()
    time.sleep(3)  # Wait for server to start
    
    # Start clients
    client_processes = []
    for client_id in range(1, NUM_CLIENTS + 1):
        client_process = start_client(client_id)
        client_processes.append(client_process)
        time.sleep(1)  # Stagger client starts
    
    print("\n" + "=" * 60)
    print("All processes started!")
    print("=" * 60)
    print(f"Server PID: {server_process.pid}")
    for i, client_process in enumerate(client_processes, 1):
        print(f"Client {i} PID: {client_process.pid}")
    print("\nPress Ctrl+C to stop all processes...")
    
    try:
        # Wait for processes
        server_process.wait()
        for client_process in client_processes:
            client_process.wait()
    except KeyboardInterrupt:
        print("\n\nStopping all processes...")
        server_process.terminate()
        for client_process in client_processes:
            client_process.terminate()
        
        # Wait a bit for graceful shutdown
        time.sleep(2)
        
        # Force kill if still running
        if server_process.poll() is None:
            server_process.kill()
        for client_process in client_processes:
            if client_process.poll() is None:
                client_process.kill()
        
        print("All processes stopped.")

if __name__ == "__main__":
    main()


