"""
Simple script to run federated learning - starts server and clients sequentially
"""
import subprocess
import sys
import time
import threading
from pathlib import Path

def run_server():
    """Run server in separate process"""
    base_dir = Path(__file__).parent.parent
    server_script = base_dir / "flower_server" / "server.py"
    
    env = {
        "SERVER_ADDRESS": "0.0.0.0",
        "SERVER_PORT": "8080",
        "NUM_ROUNDS": "10",
        "MIN_CLIENTS": "3",
        "FRACTION_FIT": "1.0",
        "FRACTION_EVALUATE": "1.0",
        "LOCAL_EPOCHS": "5",
        "BATCH_SIZE": "32",
        "LEARNING_RATE": "0.001"
    }
    
    print("Starting server...")
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env={**os.environ, **env},
        cwd=str(base_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Print server output
    def print_output():
        for line in process.stdout:
            print(f"[SERVER] {line.rstrip()}")
    
    thread = threading.Thread(target=print_output, daemon=True)
    thread.start()
    
    return process

def run_client(client_id):
    """Run client"""
    base_dir = Path(__file__).parent.parent
    client_script = base_dir / "flower_client" / "client.py"
    
    env = {
        "FLOWER_SERVER_URL": "localhost:8080",
        "LOCAL_EPOCHS": "5",
        "BATCH_SIZE": "32",
        "LEARNING_RATE": "0.001"
    }
    
    print(f"Starting client {client_id}...")
    process = subprocess.Popen(
        [sys.executable, str(client_script),
         "--client-id", str(client_id),
         "--server-address", "localhost:8080",
         "--data-dir", "output"],
        env={**os.environ, **env},
        cwd=str(base_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Print client output
    def print_output():
        for line in process.stdout:
            print(f"[CLIENT-{client_id}] {line.rstrip()}")
    
    thread = threading.Thread(target=print_output, daemon=True)
    thread.start()
    
    return process

if __name__ == "__main__":
    import os
    
    print("=" * 70)
    print("Federated Learning Training")
    print("=" * 70)
    
    # Start server
    server = run_server()
    time.sleep(10)  # Wait for server
    
    # Start clients
    clients = []
    for i in range(1, 4):
        client = run_client(i)
        clients.append(client)
        time.sleep(3)
    
    print("\nAll processes started. Training in progress...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Wait for server
        server.wait()
        print("\nServer completed!")
        
        # Wait for clients
        for i, client in enumerate(clients, 1):
            client.wait(timeout=5)
            print(f"Client {i} completed")
        
        # Check models
        model_dir = Path(__file__).parent.parent / "flower_server" / "models"
        if model_dir.exists():
            models = list(model_dir.glob("*.pt"))
            print(f"\nModels created: {len(models)}")
            for m in models:
                print(f"  - {m.name}")
    except KeyboardInterrupt:
        print("\nStopping...")
        server.terminate()
        for c in clients:
            c.terminate()
