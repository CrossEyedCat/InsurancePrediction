"""
Script to start federated learning training
Starts server first, then clients
"""
import subprocess
import sys
import time
import os
from pathlib import Path

SERVER_ADDRESS = "localhost"
SERVER_PORT = "8080"
NUM_CLIENTS = 3

def main():
    print("=" * 70)
    print("Starting Federated Learning Training")
    print("=" * 70)
    
    base_dir = Path(__file__).parent.parent
    
    # Set environment variables
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
    
    # Start server
    print("\n[1/4] Starting Flower Server...")
    server_script = base_dir / "flower_server" / "server.py"
    server_process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        cwd=str(base_dir)
    )
    print(f"Server PID: {server_process.pid}")
    print("Waiting for server to initialize...")
    time.sleep(8)  # Give server time to start
    
    # Start clients
    client_processes = []
    client_script = base_dir / "flower_client" / "client.py"
    
    for client_id in range(1, NUM_CLIENTS + 1):
        print(f"\n[{client_id+1}/4] Starting Client {client_id}...")
        client_env = env.copy()
        client_env["FLOWER_SERVER_URL"] = f"{SERVER_ADDRESS}:{SERVER_PORT}"
        
        client_process = subprocess.Popen(
            [sys.executable, str(client_script),
             "--client-id", str(client_id),
             "--server-address", f"{SERVER_ADDRESS}:{SERVER_PORT}",
             "--data-dir", "output"],
            env=client_env,
            cwd=str(base_dir)
        )
        client_processes.append(client_process)
        print(f"Client {client_id} PID: {client_process.pid}")
        time.sleep(2)  # Stagger client starts
    
    print("\n" + "=" * 70)
    print("All processes started!")
    print("=" * 70)
    print(f"Server PID: {server_process.pid}")
    for i, cp in enumerate(client_processes, 1):
        print(f"Client {i} PID: {cp.pid}")
    print("\nTraining in progress...")
    print("This will take several minutes. Please wait...")
    print("=" * 70)
    
    # Wait for server to complete
    try:
        server_code = server_process.wait()
        print(f"\nServer completed with exit code: {server_code}")
        
        # Wait for clients
        for i, cp in enumerate(client_processes, 1):
            if cp.poll() is None:
                cp.wait(timeout=10)
            print(f"Client {i} completed")
        
        # Check for models
        model_dir = base_dir / "flower_server" / "models"
        if model_dir.exists():
            models = list(model_dir.glob("*.pt"))
            if models:
                print(f"\n{'='*70}")
                print("SUCCESS! Models created:")
                print("=" * 70)
                for model in models:
                    size_mb = model.stat().st_size / (1024 * 1024)
                    print(f"  - {model.name} ({size_mb:.2f} MB)")
            else:
                print("\nWARNING: No models found!")
        else:
            print("\nWARNING: Models directory not found!")
            
    except KeyboardInterrupt:
        print("\n\nStopping all processes...")
        server_process.terminate()
        for cp in client_processes:
            cp.terminate()
        time.sleep(2)
        if server_process.poll() is None:
            server_process.kill()
        for cp in client_processes:
            if cp.poll() is None:
                cp.kill()
        print("All processes stopped.")

if __name__ == "__main__":
    main()
