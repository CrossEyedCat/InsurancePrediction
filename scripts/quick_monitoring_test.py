"""
Quick test script for monitoring - checks if APIs are accessible
"""
import requests
import time
import sys


def test_server_monitoring():
    """Test server monitoring API"""
    print("Testing Server Monitoring API (http://localhost:8082)...")
    
    try:
        # Health check
        response = requests.get("http://localhost:8082/health", timeout=5)
        if response.status_code == 200:
            print("  [OK] Server health check passed")
        else:
            print(f"  [FAIL] Server health check failed: {response.status_code}")
            return False
        
        # Status
        response = requests.get("http://localhost:8082/monitoring/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Server status retrieved")
            print(f"      Current round: {data.get('current_round')}")
            print(f"      Total rounds: {data.get('total_rounds')}")
            print(f"      Is training: {data.get('is_training')}")
        else:
            print(f"  [FAIL] Server status failed: {response.status_code}")
            return False
        
        # History
        response = requests.get("http://localhost:8082/monitoring/history", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Server history retrieved ({len(data.get('history', []))} entries)")
        else:
            print(f"  [FAIL] Server history failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("  [ERROR] Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def test_client_monitoring():
    """Test client monitoring API"""
    print("\nTesting Client Monitoring API (http://localhost:8081)...")
    
    try:
        # Health check
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code == 200:
            print("  [OK] Client health check passed")
        else:
            print(f"  [FAIL] Client health check failed: {response.status_code}")
            return False
        
        # Status
        response = requests.get("http://localhost:8081/monitoring/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Client status retrieved")
            print(f"      Client ID: {data.get('client_id')}")
            print(f"      Total trainings: {data.get('total_trainings')}")
            print(f"      Is training: {data.get('is_training')}")
        else:
            print(f"  [FAIL] Client status failed: {response.status_code}")
            return False
        
        # History
        response = requests.get("http://localhost:8081/monitoring/history?limit=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Client history retrieved ({len(data.get('history', []))} entries)")
        else:
            print(f"  [FAIL] Client history failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("  [ERROR] Cannot connect to client. Is it running?")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Main function"""
    print("=" * 70)
    print("Quick Monitoring Test")
    print("=" * 70)
    print("\nMake sure server and client are running:")
    print("  Server: python flower_server/server_with_monitoring.py")
    print("  Client: python flower_client/client_with_api.py --client-id 1")
    print("\nWaiting 3 seconds...")
    time.sleep(3)
    
    server_ok = test_server_monitoring()
    client_ok = test_client_monitoring()
    
    print("\n" + "=" * 70)
    if server_ok and client_ok:
        print("All monitoring tests passed!")
    else:
        print("Some tests failed. Check if server and client are running.")
    print("=" * 70)
    
    return 0 if (server_ok and client_ok) else 1


if __name__ == "__main__":
    sys.exit(main())

