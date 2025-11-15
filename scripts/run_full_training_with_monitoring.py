"""
Full training with monitoring - starts server, multiple clients, and monitors the process
"""
import subprocess
import sys
import time
import os
from pathlib import Path
import requests
import json
from datetime import datetime


def start_server_with_monitoring():
    """Start Flower server with monitoring"""
    print("=" * 70)
    print("Starting Flower Server with Monitoring...")
    print("=" * 70)
    
    server_script = Path(__file__).parent.parent / "flower_server" / "server_with_monitoring.py"
    
    env = os.environ.copy()
    env["SERVER_ADDRESS"] = "127.0.0.1"  # Use localhost on Windows
    env["SERVER_PORT"] = "8080"
    env["HTTP_PORT"] = "8082"
    env["NUM_ROUNDS"] = "5"
    env["MIN_CLIENTS"] = "3"
    env["FRACTION_FIT"] = "1.0"
    env["FRACTION_EVALUATE"] = "1.0"
    env["MIN_AVAILABLE_CLIENTS"] = "3"
    
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    print(f"Server started with PID: {process.pid}")
    return process


def start_client_with_monitoring(client_id, http_port_base=8081):
    """Start Flower client with monitoring"""
    # Use ports 8081, 8083, 8084 (skip 8082 which is used by server)
    if client_id == 1:
        http_port = 8081
    elif client_id == 2:
        http_port = 8083
    else:
        http_port = 8084
    
    client_script = Path(__file__).parent.parent / "flower_client" / "client_with_api.py"
    
    env = os.environ.copy()
    env["FLOWER_SERVER_URL"] = "localhost:8080"
    env["LOCAL_EPOCHS"] = "3"
    env["BATCH_SIZE"] = "32"
    env["LEARNING_RATE"] = "0.001"
    env["HTTP_PORT"] = str(http_port)
    
    process = subprocess.Popen(
        [sys.executable, str(client_script),
         "--client-id", str(client_id),
         "--server-address", "localhost:8080",
         "--data-dir", "output",
         "--http-port", str(http_port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    print(f"Client {client_id} started with PID: {process.pid} (HTTP API: {http_port})")
    return process, http_port


def wait_for_api(base_url, timeout=60, service_name="API"):
    """Wait for HTTP API to be ready"""
    print(f"Waiting for {service_name} at {base_url}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print(f"{service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(".", end="", flush=True)
    
    print(f"\n{service_name} did not become ready in time")
    return False


def monitor_training(server_url, client_urls, duration=300):
    """Monitor training progress"""
    print("\n" + "=" * 70)
    print("Monitoring Training Progress...")
    print("=" * 70)
    
    start_time = time.time()
    last_round = -1
    
    while time.time() - start_time < duration:
        try:
            # Check server status
            response = requests.get(f"{server_url}/monitoring/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                current_round = status.get("current_round")
                is_training = status.get("is_training", False)
                
                if current_round != last_round:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Round {current_round} - Training: {is_training}")
                    last_round = current_round
                    
                    # Get round details
                    if current_round:
                        try:
                            round_response = requests.get(
                                f"{server_url}/monitoring/round/{current_round}", 
                                timeout=5
                            )
                            if round_response.status_code == 200:
                                round_data = round_response.json()
                                if "aggregated_metrics" in round_data:
                                    metrics = round_data["aggregated_metrics"]
                                    if "loss" in metrics:
                                        print(f"  Aggregated Loss: {metrics['loss']:.6f}")
                        except:
                            pass
                
                # Check client statuses
                for i, client_url in enumerate(client_urls, 1):
                    try:
                        client_response = requests.get(
                            f"{client_url}/monitoring/status", 
                            timeout=2
                        )
                        if client_response.status_code == 200:
                            client_status = client_response.json()
                            if client_status.get("is_training"):
                                print(f"  Client {i}: Training...")
                    except:
                        pass
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\nMonitoring interrupted by user")
            break
        except Exception as e:
            print(f"\nError monitoring: {e}")
            time.sleep(5)


def print_final_summary(server_url, client_urls):
    """Print final training summary"""
    print("\n" + "=" * 70)
    print("Final Training Summary")
    print("=" * 70)
    
    # Server summary
    try:
        response = requests.get(f"{server_url}/monitoring/summary", timeout=5)
        if response.status_code == 200:
            summary = response.json()
            print("\nServer Summary:")
            print(f"  Total rounds: {summary.get('total_rounds', 0)}")
            print(f"  Average loss: {summary.get('average_loss', 'N/A')}")
            print(f"  Latest loss: {summary.get('latest_loss', 'N/A')}")
            print(f"  Min loss: {summary.get('min_loss', 'N/A')}")
    except Exception as e:
        print(f"Error getting server summary: {e}")
    
    # Client summaries
    print("\nClient Summaries:")
    for i, client_url in enumerate(client_urls, 1):
        try:
            response = requests.get(f"{client_url}/monitoring/summary", timeout=5)
            if response.status_code == 200:
                summary = response.json()
                print(f"\n  Client {i}:")
                print(f"    Total trainings: {summary.get('total_trainings', 0)}")
                print(f"    Average training loss: {summary.get('average_training_loss', 'N/A')}")
                print(f"    Latest training loss: {summary.get('latest_training_loss', 'N/A')}")
        except Exception as e:
            print(f"  Client {i}: Error - {e}")


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("Full Training with Monitoring")
    print("=" * 70)
    print("\nThis will start:")
    print("  - Flower server with monitoring (port 8080, HTTP API: 8082)")
    print("  - 3 Flower clients with monitoring (HTTP APIs: 8081, 8083, 8084)")
    print("  - Training for 5 rounds")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    server_process = None
    client_processes = []
    client_urls = []
    
    try:
        # Start server
        server_process = start_server_with_monitoring()
        time.sleep(5)
        
        if not wait_for_api("http://localhost:8082", service_name="Server API"):
            print("Failed to start server API")
            return
        
        # Start clients
        print("\n" + "=" * 70)
        print("Starting Clients...")
        print("=" * 70)
        
        for client_id in [1, 2, 3]:
            process, http_port = start_client_with_monitoring(client_id)
            client_processes.append(process)
            client_urls.append(f"http://localhost:{http_port}")
            time.sleep(3)
        
        # Wait for clients to be ready
        print("\nWaiting for clients to initialize...")
        all_ready = True
        for i, url in enumerate(client_urls, 1):
            if not wait_for_api(url, timeout=60, service_name=f"Client {i} API"):
                all_ready = False
        
        if not all_ready:
            print("Some clients failed to start. Continuing anyway...")
        
        # Monitor training
        print("\n" + "=" * 70)
        print("Training Started - Monitoring Progress")
        print("=" * 70)
        print("Press Ctrl+C to stop monitoring (processes will continue)")
        print()
        
        monitor_training("http://localhost:8082", client_urls, duration=600)
        
        # Print final summary
        print_final_summary("http://localhost:8082", client_urls)
        
        print("\n" + "=" * 70)
        print("Training Complete!")
        print("=" * 70)
        print("\nProcesses are still running.")
        print("Press Ctrl+C to stop all processes.")
        
        # Keep processes running
        try:
            server_process.wait()
            for proc in client_processes:
                proc.wait()
        except KeyboardInterrupt:
            print("\n\nStopping all processes...")
            if server_process:
                server_process.terminate()
            for proc in client_processes:
                proc.terminate()
            if server_process:
                server_process.wait()
            for proc in client_processes:
                proc.wait()
            print("All processes stopped.")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup
        if server_process:
            server_process.terminate()
        for proc in client_processes:
            proc.terminate()


if __name__ == "__main__":
    main()

