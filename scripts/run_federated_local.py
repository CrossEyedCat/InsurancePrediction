"""
Improved script to run federated learning locally with better output handling
"""
import subprocess
import sys
import time
import os
import threading
from pathlib import Path
import queue

# Configuration
SERVER_ADDRESS = "localhost"
SERVER_PORT = "8080"
NUM_CLIENTS = 3
DATA_DIR = "output"

def print_output(pipe, prefix):
    """Print output from pipe with prefix"""
    try:
        for line in iter(pipe.readline, ''):
            if line:
                print(f"[{prefix}] {line.rstrip()}")
    except Exception as e:
        print(f"[{prefix}] Error reading output: {e}")

def start_server():
    """Start Flower server"""
    print("=" * 60)
    print("Starting Flower Server")
    print("=" * 60)
    
    server_script = Path(__file__).parent.parent / "flower_server" / "server.py"
    
    env = os.environ.copy()
    env["SERVER_ADDRESS"] = SERVER_ADDRESS
    env["SERVER_PORT"] = SERVER_PORT
    env["NUM_ROUNDS"] = "5"  # Reduced for testing
    env["MIN_CLIENTS"] = "3"
    env["FRACTION_FIT"] = "1.0"
    env["FRACTION_EVALUATE"] = "1.0"
    env["LOCAL_EPOCHS"] = "3"  # Reduced for testing
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    # Start thread to print server output
    thread = threading.Thread(target=print_output, args=(process.stdout, "SERVER"))
    thread.daemon = True
    thread.start()
    
    print(f"Server started with PID: {process.pid}")
    return process

def start_client(client_id):
    """Start Flower client"""
    print(f"\nStarting Client {client_id}")
    
    client_script = Path(__file__).parent.parent / "flower_client" / "client.py"
    
    env = os.environ.copy()
    env["FLOWER_SERVER_URL"] = f"{SERVER_ADDRESS}:{SERVER_PORT}"
    env["LOCAL_EPOCHS"] = "3"  # Reduced for testing
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    
    process = subprocess.Popen(
        [sys.executable, str(client_script), 
         "--client-id", str(client_id),
         "--server-address", f"{SERVER_ADDRESS}:{SERVER_PORT}",
         "--data-dir", DATA_DIR],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    # Start thread to print client output
    thread = threading.Thread(target=print_output, args=(process.stdout, f"CLIENT-{client_id}"))
    thread.daemon = True
    thread.start()
    
    print(f"Client {client_id} started with PID: {process.pid}")
    return process

def check_data_split():
    """Check data split between clients"""
    print("\n" + "=" * 60)
    print("Checking Data Split")
    print("=" * 60)
    
    try:
        import pandas as pd
        from flower_client.data_loader import DataLoaderClient
        
        for client_id in range(1, 4):
            loader = DataLoaderClient(client_id, DATA_DIR)
            df = loader.load_data()
            print(f"Client {client_id}: {len(df)} samples (patient IDs {loader.start_idx+1}-{loader.end_idx})")
        
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"Warning: Could not check data split: {e}\n")

def main():
    """Main function"""
    print("=" * 60)
    print("Federated Learning - Local Test")
    print("=" * 60)
    print(f"Server: {SERVER_ADDRESS}:{SERVER_PORT}")
    print(f"Clients: {NUM_CLIENTS}")
    print(f"Data directory: {DATA_DIR}")
    
    # Check if data directory exists
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        print(f"\nError: Data directory '{DATA_DIR}' not found!")
        print("Please run the data generation scripts first.")
        return
    
    # Check data split
    check_data_split()
    
    # Start server
    print("Starting server...")
    server_process = start_server()
    time.sleep(5)  # Wait for server to start
    
    # Start clients
    print("\nStarting clients...")
    client_processes = []
    for client_id in range(1, NUM_CLIENTS + 1):
        client_process = start_client(client_id)
        client_processes.append(client_process)
        time.sleep(2)  # Stagger client starts
    
    print("\n" + "=" * 60)
    print("All processes started!")
    print("=" * 60)
    print(f"Server PID: {server_process.pid}")
    for i, client_process in enumerate(client_processes, 1):
        print(f"Client {i} PID: {client_process.pid}")
    print("\nTraining in progress... (Press Ctrl+C to stop)")
    print("=" * 60 + "\n")
    
    try:
        # Wait for server to complete
        server_process.wait()
        print("\n" + "=" * 60)
        print("Server completed!")
        print("=" * 60)
        
        # Wait a bit for clients to finish
        time.sleep(2)
        
        # Stop clients if still running
        for client_process in client_processes:
            if client_process.poll() is None:
                print(f"Stopping client {client_processes.index(client_process) + 1}...")
                client_process.terminate()
                client_process.wait(timeout=5)
        
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
    
    # Check for saved models
    model_dir = Path(__file__).parent.parent / "flower_server" / "models"
    if model_dir.exists():
        models = list(model_dir.glob("*.pt"))
        if models:
            print(f"\nModels saved: {len(models)}")
            for model in models:
                print(f"  - {model.name}")

if __name__ == "__main__":
    main()

