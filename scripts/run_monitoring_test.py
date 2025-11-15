"""
Script to run Flower server with monitoring, client with monitoring, and test monitoring API
"""
import subprocess
import sys
import time
import os
from pathlib import Path
import requests


def start_server_with_monitoring():
    """Start Flower server with monitoring"""
    print("=" * 70)
    print("Starting Flower Server with Monitoring...")
    print("=" * 70)
    
    server_script = Path(__file__).parent.parent / "flower_server" / "server_with_monitoring.py"
    
    env = os.environ.copy()
    env["SERVER_ADDRESS"] = "0.0.0.0"
    env["SERVER_PORT"] = "8080"
    env["HTTP_PORT"] = "8082"
    env["NUM_ROUNDS"] = "5"
    env["MIN_CLIENTS"] = "1"  # Allow single client for testing
    env["FRACTION_FIT"] = "1.0"
    env["FRACTION_EVALUATE"] = "1.0"
    env["MIN_AVAILABLE_CLIENTS"] = "1"
    
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    
    print(f"Server started with PID: {process.pid}")
    print("Waiting for server to initialize...")
    time.sleep(5)
    
    return process


def start_client_with_monitoring(client_id=1, http_port=8081):
    """Start Flower client with monitoring"""
    print("\n" + "=" * 70)
    print(f"Starting Flower Client {client_id} with Monitoring...")
    print("=" * 70)
    
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
    
    print(f"Client {client_id} started with PID: {process.pid}")
    print(f"HTTP API available on port {http_port}")
    print("Waiting for client to initialize...")
    time.sleep(8)  # Increased wait time for data loading
    
    return process


def wait_for_api(base_url, timeout=45, service_name="API"):
    """Wait for HTTP API to be ready"""
    print(f"\nWaiting for {service_name} at {base_url}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print(f"{service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        print(".", end="", flush=True)
    
    print(f"\n{service_name} did not become ready in time")
    return False


def test_monitoring():
    """Test monitoring APIs"""
    print("\n" + "=" * 70)
    print("Testing Monitoring APIs...")
    print("=" * 70)
    
    test_script = Path(__file__).parent / "test_monitoring.py"
    
    result = subprocess.run(
        [sys.executable, str(test_script),
         "--server-url", "http://localhost:8082",
         "--client-url", "http://localhost:8081"],
        capture_output=False
    )
    
    return result.returncode == 0


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("Flower Server + Client + Monitoring Test")
    print("=" * 70)
    
    server_process = None
    client_process = None
    
    try:
        # Start server
        server_process = start_server_with_monitoring()
        
        # Wait for server API
        if not wait_for_api("http://localhost:8082", service_name="Server API"):
            print("Failed to start server API. Check server logs.")
            return
        
        # Start client
        client_process = start_client_with_monitoring(client_id=1, http_port=8081)
        
        # Wait for client API
        if not wait_for_api("http://localhost:8081", service_name="Client API"):
            print("Failed to start client API. Check client logs.")
            return
        
        # Test monitoring
        print("\n")
        success = test_monitoring()
        
        if success:
            print("\n" + "=" * 70)
            print("All monitoring tests passed!")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("Some monitoring tests failed")
            print("=" * 70)
        
        print("\nServer and client are running with monitoring.")
        print("Monitoring endpoints:")
        print("  Server: http://localhost:8082/monitoring/status")
        print("  Client: http://localhost:8081/monitoring/status")
        print("\nPress Ctrl+C to stop.")
        
        # Keep processes running
        try:
            server_process.wait()
            client_process.wait()
        except KeyboardInterrupt:
            print("\n\nStopping processes...")
            if server_process:
                server_process.terminate()
            if client_process:
                client_process.terminate()
            if server_process:
                server_process.wait()
            if client_process:
                client_process.wait()
            print("Processes stopped.")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup
        if server_process:
            server_process.terminate()
        if client_process:
            client_process.terminate()


if __name__ == "__main__":
    main()

