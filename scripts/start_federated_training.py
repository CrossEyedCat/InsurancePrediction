"""
Script to start federated learning training
Properly coordinates server and clients
"""
import subprocess
import sys
import time
import os
import signal
from pathlib import Path

# Configuration
SERVER_ADDRESS = "localhost"
SERVER_PORT = "8080"
NUM_CLIENTS = 3
DATA_DIR = "output"

processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    print("\n\nStopping all processes...")
    for proc in processes:
        try:
            proc.terminate()
        except:
            pass
    time.sleep(2)
    for proc in processes:
        try:
            if proc.poll() is None:
                proc.kill()
        except:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    """Main function"""
    print("=" * 70)
    print("Federated Learning Training")
    print("=" * 70)
    print(f"Server: {SERVER_ADDRESS}:{SERVER_PORT}")
    print(f"Clients: {NUM_CLIENTS}")
    print(f"Data directory: {DATA_DIR}")
    print()
    
    # Check data directory
    if not Path(DATA_DIR).exists():
        print(f"ERROR: Data directory '{DATA_DIR}' not found!")
        return
    
    # Set environment variables
    env = os.environ.copy()
    env["SERVER_ADDRESS"] = SERVER_ADDRESS
    env["SERVER_PORT"] = SERVER_PORT
    env["NUM_ROUNDS"] = "5"
    env["MIN_CLIENTS"] = "3"
    env["FRACTION_FIT"] = "1.0"
    env["FRACTION_EVALUATE"] = "1.0"
    env["MIN_AVAILABLE_CLIENTS"] = "3"
    env["LOCAL_EPOCHS"] = "3"
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    
    # Start server
    print("Starting server...")
    server_script = Path(__file__).parent.parent / "flower_server" / "server.py"
    server_proc = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    processes.append(server_proc)
    print(f"Server started (PID: {server_proc.pid})")
    
    # Wait for server to be ready
    print("Waiting for server to initialize...")
    time.sleep(5)
    
    # Start clients
    print("\nStarting clients...")
    client_script = Path(__file__).parent.parent / "flower_client" / "client.py"
    
    for client_id in range(1, NUM_CLIENTS + 1):
        print(f"  Starting client {client_id}...")
        client_env = env.copy()
        client_env["FLOWER_SERVER_URL"] = f"{SERVER_ADDRESS}:{SERVER_PORT}"
        
        client_proc = subprocess.Popen(
            [sys.executable, str(client_script),
             "--client-id", str(client_id),
             "--server-address", f"{SERVER_ADDRESS}:{SERVER_PORT}",
             "--data-dir", DATA_DIR],
            env=client_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(client_proc)
        print(f"  Client {client_id} started (PID: {client_proc.pid})")
        time.sleep(2)  # Stagger client starts
    
    print("\n" + "=" * 70)
    print("All processes started!")
    print("=" * 70)
    print(f"Server PID: {server_proc.pid}")
    for i, proc in enumerate(processes[1:], 1):
        print(f"Client {i} PID: {proc.pid}")
    print("\nTraining in progress...")
    print("Press Ctrl+C to stop\n")
    print("=" * 70)
    
    # Monitor server output
    try:
        for line in iter(server_proc.stdout.readline, ''):
            if line:
                print(f"[SERVER] {line.rstrip()}")
            if server_proc.poll() is not None:
                break
    except KeyboardInterrupt:
        pass
    
    # Wait for server to complete
    print("\nWaiting for server to complete...")
    server_proc.wait()
    
    # Wait a bit for clients
    time.sleep(3)
    
    # Stop clients if still running
    for i, proc in enumerate(processes[1:], 1):
        if proc.poll() is None:
            print(f"Stopping client {i}...")
            proc.terminate()
            proc.wait(timeout=5)
    
    print("\n" + "=" * 70)
    print("Training completed!")
    print("=" * 70)
    
    # Check for models
    model_dir = Path(__file__).parent.parent / "flower_server" / "models"
    if model_dir.exists():
        models = list(model_dir.glob("*.pt"))
        if models:
            print(f"\nModels created: {len(models)}")
            for model in models:
                size_mb = model.stat().st_size / (1024 * 1024)
                print(f"  - {model.name} ({size_mb:.2f} MB)")
        else:
            print("\nNo models found - training may have failed")
    else:
        print("\nModel directory not found")

if __name__ == "__main__":
    main()

