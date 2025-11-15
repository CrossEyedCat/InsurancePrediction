"""
Test script for client HTTP API
Tests external service requests to trigger training
"""
import requests
import json
import time


def test_client_api(base_url: str = "http://localhost:8081"):
    """Test client HTTP API endpoints"""
    
    print("=" * 70)
    print("Testing Flower Client HTTP API")
    print("=" * 70)
    print(f"Base URL: {base_url}\n")
    
    # Test health endpoint
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   [OK] Health check passed")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"   [FAIL] Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [ERROR] Connection error - is the client running?")
        return
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test status endpoint
    print("2. Testing /status endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            print("   [OK] Status retrieved")
            data = response.json()
            print(f"   Client ID: {data.get('client_id')}")
            print(f"   Training Status: {data.get('training_status')}")
        else:
            print(f"   [FAIL] Status request failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test model info endpoint
    print("3. Testing /model/info endpoint...")
    try:
        response = requests.get(f"{base_url}/model/info", timeout=5)
        if response.status_code == 200:
            print("   [OK] Model info retrieved")
            data = response.json()
            print(f"   Model Input Size: {data.get('model', {}).get('input_size')}")
            print(f"   Total Parameters: {data.get('model', {}).get('total_parameters')}")
        else:
            print(f"   [FAIL] Model info request failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test trigger training endpoint
    print("4. Testing /train/trigger endpoint...")
    try:
        training_config = {
            "local_epochs": 3,
            "learning_rate": 0.001,
            "batch_size": 32
        }
        response = requests.post(
            f"{base_url}/train/trigger",
            json=training_config,
            timeout=5
        )
        if response.status_code == 200:
            print("   [OK] Training trigger request sent")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Configuration: {data.get('configuration')}")
        elif response.status_code == 409:
            print("   [WARN] Training already in progress")
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"   [FAIL] Training trigger failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 70)
    print("API Testing Complete")
    print("=" * 70)
    print("\nNote: The /train/trigger endpoint updates configuration.")
    print("Actual training happens when Flower server initiates a federated learning round.")


if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8081"
    test_client_api(base_url)

